/** Placeholder query result used before real data has loaded. */
const empty = {
  rows: [{}],
  cols: [{}],
  body: [[{}]],
  length: 0,
  formatHints: {},
};

/**
 * Extracts the URL-ready parts of a query object.
 *
 * Fields are encoded as a comma-separated string where each entry is the
 * field's path, optionally prefixed with "&" when pivoted, and suffixed with
 * "+N" (ascending) or "-N" (descending) for sorted fields where N is the
 * sort priority.  Filters are encoded as URL query-string parameters of the
 * form "path__lookup=value".
 *
 * @param {object} query - The query state object.
 * @returns {{ model: string, fields: string, query: string, limit: number }}
 */
function getPartsForQuery(query) {
  return {
    model: query.model,
    fields: query.fields
      .map(
        (f) =>
          (f.pivoted ? "&" : "") +
          f.pathStr +
          { asc: `+${f.priority}`, dsc: `-${f.priority}`, null: "" }[f.sort],
      )
      .join(","),
    query: query.filters
      .map((f) => `${f.pathStr}__${f.lookup}=${encodeURIComponent(f.value)}`)
      .join("&"),
    limit: query.limit,
  };
}

/**
 * Returns a relative URL for the given query and media type.
 *
 * @param {object} query - The query state object.
 * @param {string} media - The media/format suffix (e.g. "json", "csv", "html").
 * @returns {string} Relative URL of the form "query/Model/fields.media?filters&limit=N".
 */
function getRelUrlForQuery(query, media) {
  const { model, fields, query: query_str, limit } = getPartsForQuery(query);
  return `query/${model}/${fields}.${media}?${query_str}&limit=${limit}`;
}

/**
 * Returns an absolute URL for the given query and media type.
 *
 * @param {string} baseUrl - The application base URL path (e.g. "/data-browser/").
 * @param {object} query - The query state object.
 * @param {string} media - The media/format suffix (e.g. "json", "csv", "html").
 * @returns {string} Absolute URL including origin.
 */
function getUrlForQuery(baseUrl, query, media) {
  const relUrl = getRelUrlForQuery(query, media);
  return `${window.location.origin}${baseUrl}${relUrl}`;
}


/**
 * Returns the index of a field within an array of fields, matched by pathStr.
 *
 * @param {object} field - Field object with a `pathStr` property.
 * @param {object[]} fields - Array of field objects to search.
 * @returns {number} Index of the matching field, or -1 if not found.
 */
function getFieldIndex(field, fields) {
  return fields.findIndex((f) => f.pathStr === field.pathStr);
}

/**
 * Decrements the priority of every field whose sort priority is greater than
 * `removedPriority`, closing the gap left when a sort is removed.
 *
 * @param {object[]} fields - Array of field objects.
 * @param {number} removedPriority - The priority that is being vacated.
 * @returns {object[]} New array with adjusted priorities.
 */
function compactSortPriorities(fields, removedPriority) {
  return fields.map((f) => ({
    ...f,
    priority:
      f.priority != null && f.priority > removedPriority
        ? f.priority - 1
        : f.priority,
  }));
}


/**
 * Wraps the current query definition and its most recent result data, and
 * provides methods for reading and mutating the query.
 *
 * The query object contains two distinct concerns:
 * - **Query definition** — model, fields, filters, limit — what to fetch.
 * - **Result data** — rows, cols, body — the data returned by the last fetch.
 *
 * All mutation methods call `setQuery` with a partial update that is merged
 * into the stored query by the caller.
 */
class Query {
  /**
   * @param {object} config - Application-level config including type and model
   *   field metadata (allModelFields, types, baseUrl, defaultRowLimit).
   * @param {object} query - The combined query definition and result data.
   *   Definition fields: model, fields, filters, limit.
   *   Result fields: rows, cols, body (populated after each fetch).
   * @param {Function} setQuery - Callback to signal that the query definition
   *   has changed.  First argument is a partial object merged into the stored
   *   query.  Optional second boolean argument (default true) indicates whether
   *   the change requires refetching the result data; pass false for
   *   layout-only changes where the existing data is still valid.
   */
  constructor(config, query, setQuery) {
    this.config = config;
    this.query = query;
    this.setQuery = setQuery;
  }

  /**
   * Resolves a double-underscore-separated field path string to the leaf
   * model-field descriptor, following relation links through each intermediate
   * model.
   *
   * @param {string} pathStr - Field path such as "author__name".
   * @returns {object|null} The model-field descriptor, or null if any segment
   *   of the path is not found.
   */
  getField(pathStr) {
    const path = pathStr.split("__");
    let model = this.query.model;
    let modelField = null;
    for (const field of path) {
      modelField = this.config.allModelFields[model].fields[field];
      if (modelField === undefined) return null;
      model = modelField.model;
    }
    return modelField;
  }

  /**
   * Returns the type descriptor for a model-field descriptor.
   *
   * @param {object} field - A model-field descriptor as returned by `getField`.
   * @returns {object} The type descriptor (lookups, defaultLookup, defaultValue, …).
   */
  getType(field) {
    return this.config.types[field.type];
  }

  /**
   * Returns the field map and metadata for the given model name.
   *
   * @param {string} model - Model name (e.g. "app.MyModel").
   * @returns {object} Object containing `fields`, `defaultFilters`, etc.
   */
  getModelFields(model) {
    return this.config.allModelFields[model];
  }

  /**
   * Returns the default filter value string for a given field, type, and lookup.
   *
   * For choice-based lookups the first available choice is used; otherwise the
   * type's own `defaultValue` is used.
   *
   * @param {object} field - Model-field descriptor.
   * @param {object} type - Type descriptor for the field.
   * @param {string} lookup - Lookup key (e.g. "equals", "contains").
   * @returns {string} The default value as a string.
   */
  getDefaultLookupValue(field, type, lookup) {
    const lookup_type = type.lookups[lookup].type;
    if (lookup_type.endsWith("choice")) return String(field.choices[0]);
    else return String(this.config.types[lookup_type].defaultValue);
  }

  /**
   * Adds (or re-adds) a field to the query, replacing any existing entry for
   * the same path.  If a sort direction is provided the new field gets the
   * next available sort priority (highest existing priority + 1).
   *
   * @param {string} pathStr - Double-underscore-separated field path.
   * @param {string|null} sort - Initial sort direction: "asc", "dsc", or null.
   */
  addField(pathStr, sort) {
    const newFields = this.query.fields.filter((f) => f.pathStr !== pathStr);
    const priorities = newFields
      .map((f) => f.priority)
      .filter((f) => f !== null);
    const newPriority = priorities.length ? Math.max(...priorities) + 1 : 0;
    newFields.push({
      pathStr: pathStr,
      sort: sort,
      priority: sort ? newPriority : null,
      pivoted: false,
    });
    this.setQuery({ fields: newFields });
  }

  /**
   * Removes a field from the query.
   *
   * A refetch is required when removing a valid row or col field, because
   * those fields participate in the collective distinct that produces the
   * pivot table's row and column headers.  Removing a body field (canPivot
   * false) or an already-invalid field does not change the result shape, so
   * no refetch is needed.
   *
   * @param {object} field - Field object from `query.fields`.
   */
  removeField(field) {
    const modelField = this.getField(field.pathStr);
    let newFields = this.query.fields.filter((f) => f.pathStr !== field.pathStr);
    if (field.sort) {
      newFields = compactSortPriorities(newFields, field.priority);
    }
    this.setQuery(
      { fields: newFields },
      !field.errorMessage && modelField.canPivot,
    );
  }

  /**
   * Moves a field one position left or right within its section (cols, rows,
   * or body).  The field's section is determined by its pivot state and
   * whether the underlying model field can be pivoted.  Does nothing if the
   * field is already at the boundary of its section.
   *
   * No refetch is needed because the same result data is valid regardless of
   * field display order.
   *
   * @param {object} field - Field object from `query.fields`.
   * @param {boolean} left - True to move left (earlier), false to move right.
   */
  moveField(field, left) {
    const modelField = this.getField(field.pathStr);

    // get the fields in their sections
    const colFields = this.colFields().slice();
    const rowFields = this.rowFields().slice();
    const bodyFields = this.bodyFields().slice();

    // pick the section our field is in
    let fields = null;
    if (field.pivoted) fields = colFields;
    else if (modelField.canPivot) fields = rowFields;
    else fields = bodyFields;

    // work out it's old and new index
    const index = getFieldIndex(field, fields);
    const newIndex = index + (left ? -1 : 1);

    // if anything changed then update our section and then
    // rebuild all the fields from the sections
    if (0 <= newIndex && newIndex < fields.length) {
      fields.splice(index, 1);
      fields.splice(newIndex, 0, field);
      this.setQuery(
        { fields: [].concat(rowFields, colFields, bodyFields) },
        false,
      );
    }
  }

  /**
   * Cycles a field's sort direction through null → asc → dsc → null.
   *
   * Keeps the sort indicies forward packed.
   *
   * @param {object} field - Field object from `query.fields`.
   */
  toggleSort(field) {
    const index = getFieldIndex(field, this.query.fields);
    const newSort = { asc: "dsc", dsc: null, null: "asc" }[field.sort];
    let newFields = this.query.fields.slice();

    if (field.sort) {
      // move any later sort fields forward
      newFields = compactSortPriorities(newFields, field.priority);
    }

    if (newSort) {
      // move all other fiels back and insert the updated one
      newFields = newFields.map((f) => ({
        ...f,
        priority: f.priority != null ? f.priority + 1 : f.priority,
      }));
      newFields[index] = { ...field, sort: newSort, priority: 0 };
    } else {
      // blank the sort on the updated field
      newFields[index] = { ...field, sort: null, priority: null };
    }

    this.setQuery({
      fields: newFields,
    });
  }

  /**
   * Toggles the `pivoted` flag on a field, moving it between the row section
   * and the col section of the pivot table.
   *
   * @param {object} field - Field object from `query.fields`.
   */
  togglePivot(field) {
    const index = getFieldIndex(field, this.query.fields);
    let newFields = this.query.fields.slice();
    newFields[index].pivoted = !newFields[index].pivoted;
    this.setQuery({
      fields: newFields,
    });
  }

  /**
   * Appends a new filter for the given field path using the type's default
   * lookup and default value.
   *
   * @param {string} pathStr - Double-underscore-separated field path.
   */
  addFilter(pathStr) {
    const field = this.getField(pathStr);
    const type = this.getType(field);
    const newFilters = this.query.filters.slice();
    newFilters.push({
      pathStr: pathStr,
      lookup: type.defaultLookup,
      value: this.getDefaultLookupValue(field, type, type.defaultLookup),
    });
    this.setQuery({ filters: newFilters });
  }

  /**
   * Constructs a filter object for a given value, choosing an appropriate
   * lookup automatically.
   *
   * - `null` maps to the "is_null" lookup (if the type supports it) with value
   *   "IsNull" or "NotNull" when negated.  "IsNull" and "NotNull" are the
   *   choice-like labels that the backend maps to Django's `__isnull=True/False`.
   * - The strings "IsNull" / "NotNull" (already an isnull-style value) map to
   *   an "equals" lookup, with the value swapped when negated.
   * - Any other value maps to "equals" or "not_equals" depending on `negate`.
   * - Returns null if no suitable lookup exists on the field's type.
   *
   * @param {string} pathStr - Double-underscore-separated field path.
   * @param {*} value - The cell value to filter on.
   * @param {boolean} negate - When true, produce an exclusion filter instead.
   * @returns {{ pathStr: string, lookup: string, value: string }|null}
   */
  filterForValue(pathStr, value, negate) {
    const lookups = this.getType(this.getField(pathStr)).lookups;
    if (value === null && lookups.hasOwnProperty("is_null"))
      return {
        pathStr: pathStr,
        lookup: "is_null",
        value: negate ? "NotNull" : "IsNull",
      };
    if (value === "IsNull" || value === "NotNull")
      return {
        pathStr: pathStr,
        lookup: "equals",
        value: negate ? { IsNull: "NotNull", NotNull: "IsNull" }[value] : value,
      };
    else if (lookups.hasOwnProperty("equals"))
      return {
        pathStr: pathStr,
        lookup: negate ? "not_equals" : "equals",
        value: String(value),
      };
    else return null;
  }

  /**
   * Appends a filter that includes rows matching `value` on the given field.
   *
   * @param {string} pathStr - Double-underscore-separated field path.
   * @param {*} value - The value to filter on.
   */
  addExactFilter(pathStr, value) {
    const newFilters = this.query.filters.slice();
    newFilters.push(this.filterForValue(pathStr, value, false));
    this.setQuery({ filters: newFilters });
  }

  /**
   * Appends a filter that excludes rows matching `value` on the given field.
   *
   * @param {string} pathStr - Double-underscore-separated field path.
   * @param {*} value - The value to exclude.
   */
  addExactExclude(pathStr, value) {
    const newFilters = this.query.filters.slice();
    newFilters.push(this.filterForValue(pathStr, value, true));
    this.setQuery({ filters: newFilters });
  }

  /**
   * Appends equality filters derived from a cell's context values, enabling
   * navigation from an aggregate view into a more specific one.
   *
   * `rows` and `cols` are lists of dicts where each dict maps a field's
   * pathStr to its value at that row/col index.  Only fields that are
   * filterable (canPivot && concrete), present in `values`, and actually
   * distinguish rows in the current result (i.e. the relevant dimension has
   * more than one distinct value for that field) produce filters.  Fields
   * with only one distinct value are already implicitly filtered and adding
   * a redundant filter would be noise.
   *
   * @param {Object.<string, *>} values - Map of pathStr → cell value for the
   *   clicked cell's row/col context.
   */
  drillDown(values) {
    const newFilters = this.query.filters.concat(
      this.query.fields
        // limit to filterable
        .filter((field) => this.getField(field.pathStr).canPivot)
        .filter((field) => this.getField(field.pathStr).concrete)
        // values is the contextually filterable stuff, so overlap with above
        .filter((field) => values.hasOwnProperty(field.pathStr))
        // and only the filters that will actually do some filtering
        .filter((field) => {
          const allValues = field.pivoted ? this.query.cols : this.query.rows;
          const fieldValues = allValues.map((row) => row[field.pathStr]);
          const uniqueValues = new Set(fieldValues);
          return uniqueValues.size > 1;
        })
        .map((field) =>
          this.filterForValue(field.pathStr, values[field.pathStr], false),
        )
        .filter((f) => f !== null),
    );
    this.setQuery({ filters: newFilters });
  }

  /**
   * Removes the filter at the given index from the filter list.
   *
   * @param {number} index - Zero-based index into `query.filters`.
   */
  removeFilter(index) {
    const newFilters = this.query.filters.slice();
    newFilters.splice(index, 1);
    this.setQuery({ filters: newFilters });
  }

  /**
   * Updates the value of an existing filter.
   *
   * @param {number} index - Zero-based index into `query.filters`.
   * @param {string} value - New filter value string.
   */
  setFilterValue(index, value) {
    const newFilters = this.query.filters.slice();
    newFilters[index] = { ...newFilters[index], value: value };
    this.setQuery({ filters: newFilters });
  }

  /**
   * Changes the lookup operator of an existing filter.  If the new lookup has
   * a different value type than the current one, the filter value is reset to
   * the new lookup's default.
   *
   * @param {number} index - Zero-based index into `query.filters`.
   * @param {string} lookup - New lookup key (e.g. "contains", "gt").
   */
  setFilterLookup(index, lookup) {
    const newFilters = this.query.filters.slice();
    const filter = newFilters[index];
    const field = this.getField(newFilters[index].pathStr);
    const type = this.getType(field);
    if (type.lookups[filter.lookup].type !== type.lookups[lookup].type) {
      filter.value = this.getDefaultLookupValue(field, type, lookup);
    }
    filter.lookup = lookup;
    this.setQuery({ filters: newFilters });
  }

  /**
   * Sets the row limit, enforcing a minimum of 1.
   *
   * @param {number|string} limit - Desired row limit (coerced to Number).
   */
  setLimit(limit) {
    limit = Number(limit);
    this.setQuery({ limit: limit > 0 ? limit : 1 });
  }

  /**
   * Switches to a different model, resetting fields to empty and filters to
   * the model's defaults.
   *
   * @param {string} model - Model name to switch to.
   */
  setModel(model) {
    this.setQuery({
      model: model,
      fields: [],
      filters: this.config.allModelFields[model].defaultFilters,
      limit: this.config.defaultRowLimit,
      ...empty,
    });
  }

  /**
   * Returns an absolute URL for the current query in the requested format.
   *
   * @param {string} media - Format suffix (e.g. "json", "csv", "html").
   * @returns {string} Absolute URL.
   */
  getUrlForMedia(media) {
    return getUrlForQuery(this.config.baseUrl, this.query, media);
  }

  /** Returns fields that have a validation error message. */
  invalidFields() {
    return this.query.fields.filter((f) => f.errorMessage);
  }

  /** Returns fields that have no validation error message. */
  validFields() {
    return this.query.fields.filter((f) => !f.errorMessage);
  }

  /** Returns valid fields that are currently pivoted (used as column headers). */
  colFields() {
    return this.validFields().filter((f) => f.pivoted);
  }

  /** Returns valid, pivot-capable fields that are not currently pivoted (used as row headers). */
  rowFields() {
    return this.validFields().filter(
      (f) => this.getField(f.pathStr).canPivot && !f.pivoted,
    );
  }

  /** Returns valid fields whose underlying model field cannot be pivoted (body/data cells). */
  bodyFields() {
    return this.validFields().filter((f) => !this.getField(f.pathStr).canPivot);
  }

  /**
   * Converts a double-underscore path string into a human-readable label by
   * joining each segment's verbose name with arrow symbols.  Relation traversals
   * use "⇒" for single-valued relations and "⇶" for to-many relations.
   *
   * @param {string} pathStr - Double-underscore-separated field path.
   * @returns {string} Human-readable path label (e.g. "Author ⇒ Name").
   */
  verbosePathStr(pathStr) {
    const path = pathStr.split("__");
    const verbosePath = [];
    let model = this.query.model;
    let field = null;
    for (const part of path) {
      field = this.config.allModelFields[model].fields[part];
      model = field.model;
      verbosePath.push(field.verboseName);
      verbosePath.push(field.toMany ? "\u21f6" : "\u21d2");
    }
    return verbosePath.slice(0, -1).join(" ");
  }

}

/**
 * Returns a CSS class name used to style a field according to its structural
 * kind, so the user can tell at a glance what sort of field they are looking at.
 *
 * The classification priority is:
 * - No `type`      → "RelatedField"    (pure relation traversal, no own value)
 * - Not `concrete` → "CalculatedField" (Python-computed, not a DB column)
 * - Not `canPivot` → "AggregateField"  (aggregate, cannot be a row/col header)
 * - No `model`     → "FunctionField"   (applies a function/transform; detected
 *                                       by absence of sub-fields, though the
 *                                       concept does not preclude sub-fields)
 * - Not `real`     → "AnnotatedField"  (ORM annotation)
 * - Otherwise      → "RealField"       (plain database column)
 *
 * @param {object} field - Model-field descriptor.
 * @returns {string} CSS class name.
 */
function getFieldClass(field) {
  if (!field.type) return "RelatedField";
  if (!field.concrete) return "CalculatedField";
  if (!field.canPivot) return "AggregateField";
  if (!field.model) return "FunctionField";
  if (!field.real) return "AnnotatedField";
  return "RealField";
}

export { Query, getPartsForQuery, getRelUrlForQuery, getUrlForQuery, getFieldClass, empty };

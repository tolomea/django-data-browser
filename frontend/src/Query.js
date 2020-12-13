const empty = {
  rows: [{}],
  cols: [{}],
  body: [[{}]],
  length: 0,
  filterErrors: [],
  parsedFilterValues: [],
  formatHints: {},
};

function getPartsForQuery(query) {
  return {
    model: query.model,
    fields: query.fields
      .map(
        (f) =>
          (f.pivoted ? "&" : "") +
          f.pathStr +
          { asc: `+${f.priority}`, dsc: `-${f.priority}`, null: "" }[f.sort]
      )
      .join(","),
    query: query.filters
      .map((f) => `${f.pathStr}__${f.lookup}=${encodeURIComponent(f.value)}`)
      .join("&"),
    limit: query.limit,
  };
}

function getRelUrlForQuery(query, media) {
  const { model, fields, query: query_str, limit } = getPartsForQuery(query);
  return `query/${model}/${fields}.${media}?${query_str}&limit=${limit}`;
}

function getUrlForQuery(baseUrl, query, media) {
  const relUrl = getRelUrlForQuery(query, media);
  return `${window.location.origin}${baseUrl}${relUrl}`;
}

class Query {
  constructor(config, query, setQuery) {
    this.config = config;
    this.query = query;
    this.setQuery = setQuery;
  }

  getField(pathStr) {
    const path = pathStr.split("__");
    let model = this.query.model;
    for (const field of path.slice(0, -1)) {
      model = this.config.allModelFields[model].fields[field].model;
    }
    return this.config.allModelFields[model].fields[path.slice(-1)];
  }

  getType(field) {
    return this.config.types[field.type];
  }

  getModelFields(model) {
    return this.config.allModelFields[model];
  }

  getDefaultLookupValue(field, type, lookup) {
    const lookup_type = type.lookups[lookup].type;
    if (lookup_type.endsWith("choice")) return String(field.choices[0]);
    else return String(this.config.types[lookup_type].defaultValue);
  }

  _getFieldIndex(field, fields) {
    return fields.findIndex((f) => f.pathStr === field.pathStr);
  }

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

  removeField(field) {
    const modelField = this.getField(field.pathStr);
    this.setQuery(
      {
        fields: this.query.fields.filter((f) => f.pathStr !== field.pathStr),
      },
      modelField.canPivot
    );
  }

  moveField(field, left) {
    const modelField = this.getField(field.pathStr);

    // get the fields in their sections
    const colFields = this.colFields().slice();
    const rowFields = this.rowFields().slice();
    const resFields = this.resFields().slice();

    // pick the section our field is in
    let fields = null;
    if (field.pivoted) fields = colFields;
    else if (modelField.canPivot || !colFields.length) fields = rowFields;
    else fields = resFields;

    // work out it's old and new index
    const index = this._getFieldIndex(field, fields);
    const newIndex = index + (left ? -1 : 1);

    // if anything changed then update our section and then
    // rebuild all the fields from the sections
    if (0 <= newIndex && newIndex < fields.length) {
      fields.splice(index, 1);
      fields.splice(newIndex, 0, field);
      this.setQuery(
        { fields: [].concat(rowFields, colFields, resFields) },
        false
      );
    }
  }

  toggleSort(field) {
    const index = this._getFieldIndex(field, this.query.fields);
    const newSort = { asc: "dsc", dsc: null, null: "asc" }[field.sort];
    let newFields = this.query.fields.slice();

    if (field.sort) {
      // move any later sort fields forward
      newFields = newFields.map((f) => ({
        ...f,
        priority:
          f.priority != null && f.priority > field.priority
            ? f.priority - 1
            : f.priority,
      }));
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

  togglePivot(field) {
    const index = this._getFieldIndex(field, this.query.fields);
    let newFields = this.query.fields.slice();
    newFields[index].pivoted = !newFields[index].pivoted;
    this.setQuery({
      fields: newFields,
    });
  }

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

  addExactFilter(pathStr, value) {
    const newFilters = this.query.filters.slice();
    newFilters.push({
      pathStr: pathStr,
      lookup: "equals",
      value: String(value),
    });
    this.setQuery({ filters: newFilters });
  }

  drillDown(values) {
    const newFilters = this.query.filters.concat(
      this.query.fields
        .filter((field) => this.getField(field.pathStr).canPivot)
        .filter((field) => values.hasOwnProperty(field.pathStr))
        .map((field) => {
          return {
            pathStr: field.pathStr,
            lookup: "equals",
            value: String(values[field.pathStr]),
          };
        })
    );
    this.setQuery({ filters: newFilters });
  }

  removeFilter(index) {
    const newFilters = this.query.filters.slice();
    newFilters.splice(index, 1);
    this.setQuery({ filters: newFilters });
  }

  setFilterValue(index, value) {
    const newFilters = this.query.filters.slice();
    newFilters[index] = { ...newFilters[index], value: value };
    this.setQuery({ filters: newFilters });
  }

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

  setLimit(limit) {
    limit = Number(limit);
    this.setQuery({ limit: limit > 0 ? limit : 1 });
  }

  setModel(model) {
    this.setQuery({
      model: model,
      fields: [],
      filters: this.config.allModelFields[model].defaultFilters,
      limit: this.config.defaultRowLimit,
      ...empty,
    });
  }

  getUrlForMedia(media) {
    return getUrlForQuery(this.config.baseUrl, this.query, media);
  }

  colFields() {
    return this.query.fields.filter((f) => f.pivoted);
  }

  rowFields() {
    if (this.colFields().length) {
      return this.query.fields.filter(
        (f) => !f.pivoted && this.getField(f.pathStr).canPivot
      );
    } else {
      return this.query.fields;
    }
  }

  resFields() {
    if (this.colFields().length) {
      return this.query.fields.filter(
        (f) => !this.getField(f.pathStr).canPivot
      );
    } else {
      return [];
    }
  }

  prettyPathStr(pathStr) {
    const path = pathStr.split("__");
    const prettyPath = [];
    let model = this.query.model;
    let field = null;
    for (const part of path) {
      field = this.config.allModelFields[model].fields[part];
      model = field.model;
      prettyPath.push(field.prettyName);
    }
    return prettyPath.join(" \u21d2 ");
  }
}

export { Query, getPartsForQuery, getRelUrlForQuery, getUrlForQuery, empty };

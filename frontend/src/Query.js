function getPartsForQuery(query) {
  return {
    model: query.model,
    fields: query.fields
      .map(
        (f) =>
          f.path +
          { asc: `+${f.priority}`, dsc: `-${f.priority}`, null: "" }[f.sort]
      )
      .join(","),
    query: query.filters
      .map((f) => `${f.path}__${f.lookup}=${f.value}`)
      .join("&"),
  };
}

function getUrlForQuery(baseUrl, query, media) {
  const parts = getPartsForQuery(query);
  const basePath = `${baseUrl}query/${parts.model}`;
  return `${window.location.origin}${basePath}/${parts.fields}.${media}?${parts.query}`;
}

class Query {
  constructor(config, query, setQuery) {
    this.config = config;
    this.query = query;
    this.setQuery = setQuery;
  }

  getField(path) {
    const parts = path.split("__");
    const field = parts.slice(-1);
    let model = this.query.model;
    for (const field of parts.slice(0, -1)) {
      model = this.config.allModelFields[model].fks[field].model;
    }
    return this.config.allModelFields[model].fields[field];
  }

  getFieldType(path) {
    return this.config.types[this.getField(path).type];
  }

  getModelFields(model) {
    return this.config.allModelFields[model];
  }

  getDefaultLookValue(fieldType) {
    return this.config.types[fieldType.lookups[fieldType.defaultLookup].type]
      .defaultValue;
  }

  addField(path) {
    const newFields = this.query.fields.slice();
    newFields.push({ path: path, sort: null });
    const newResults = this.query.results.map((row) => row.concat([""]));
    this.setQuery({ fields: newFields, results: newResults });
  }

  removeField(index) {
    const newFields = this.query.fields.slice();
    newFields.splice(index, 1);
    const newResults = this.query.results.map((row) =>
      row.slice(0, index).concat(row.slice(index + 1))
    );
    this.setQuery({ fields: newFields, results: newResults });
  }

  toggleSort(index) {
    const field = this.query.fields[index];
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

  addFilter(path) {
    const fieldType = this.getFieldType(path);
    const newFilters = this.query.filters.slice();
    newFilters.push({
      errorMessage: null,
      path: path,
      lookup: fieldType.defaultLookup,
      value: this.getDefaultLookValue(fieldType),
    });
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
    newFilters[index] = { ...newFilters[index], lookup: lookup };
    this.setQuery({ filters: newFilters });
  }

  setModel(model) {
    this.setQuery({
      model: model,
      fields: [],
      filters: [],
      results: [],
    });
  }

  getUrlForSave() {
    if (this.config.adminUrl === null) return null;
    const parts = getPartsForQuery(this.query);
    parts.model_name = parts.model;
    const queryString = new URLSearchParams(parts).toString();
    return `${window.location.origin}${this.config.adminUrl}?${queryString}`;
  }

  getUrlForMedia(media) {
    return getUrlForQuery(this.config.baseUrl, this.query, media);
  }
}

export { Query, getPartsForQuery, getUrlForQuery };

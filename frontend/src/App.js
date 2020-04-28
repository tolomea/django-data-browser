import React from "react";
import "./App.css";
import Page from "./Components";
const assert = require("assert");
let controller;

function getAPIforWindow() {
  const location = window.location;
  const htmlUrl = location.origin + location.pathname;
  assert(htmlUrl.slice(-4) === "html");
  const jsonUrl = htmlUrl.slice(0, -4) + "json";
  return jsonUrl + location.search;
}

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      fields: [],
      filters: [],
    };
  }

  addField(path) {
    const newFields = this.state.fields.slice();
    newFields.push({ name: path, sort: null });
    const newData = this.state.data.map((row) => row.concat([""]));
    this.handleQueryChange({ fields: newFields, data: newData });
  }

  removeField(index) {
    const newFields = this.state.fields.slice();
    newFields.splice(index, 1);
    const newData = this.state.data.map((row) =>
      row.slice(0, index).concat(row.slice(index + 1))
    );
    console.log(this.state.data);
    console.log(newData);
    this.handleQueryChange({ fields: newFields, data: newData });
  }

  toggleSort(index) {
    const field = this.state.fields[index];
    const newFields = this.state.fields.slice();
    newFields[index] = {
      ...field,
      sort: { asc: "dsc", dsc: null, null: "asc" }[field.sort],
    };
    this.handleQueryChange({
      fields: newFields,
    });
  }

  addFilter(path) {
    const fieldType = this.getFieldType(path);
    const newFilters = this.state.filters.slice();
    newFilters.push({
      errorMessage: null,
      name: path,
      lookup: fieldType.defaultLookup,
      value: this.props.types[fieldType.lookups[fieldType.defaultLookup].type]
        .defaultValue,
    });
    this.handleQueryChange({ filters: newFilters });
  }

  removeFilter(index) {
    const newFilters = this.state.filters.slice();
    newFilters.splice(index, 1);
    this.handleQueryChange({ filters: newFilters });
  }

  setFilterValue(index, value) {
    const newFilters = this.state.filters.slice();
    newFilters[index] = { ...newFilters[index], value: value };
    this.handleQueryChange({ filters: newFilters });
  }

  setFilterLookup(index, lookup) {
    const newFilters = this.state.filters.slice();
    newFilters[index] = { ...newFilters[index], lookup: lookup };
    this.handleQueryChange({ filters: newFilters });
  }

  fetchData(url) {
    if (controller) controller.abort();
    controller = new AbortController();

    fetch(url, { signal: controller.signal })
      .then((res) => res.json())
      .then(
        (result) => {
          this.setState(result);
        },
        (error) => {
          this.setState({
            error,
          });
        }
      );
  }

  componentDidMount() {
    this.fetchData(getAPIforWindow());
    window.onpopstate = (e) => {
      this.fetchData(getAPIforWindow());
    };
  }

  handleQueryChange(queryChange) {
    const newState = { ...this.state, ...queryChange };
    this.setState(queryChange);
    window.history.pushState(
      null,
      null,
      this.getUrlForQuery(newState.fields, newState.filters, "html")
    );
    this.fetchData(this.getUrlForQuery(newState.fields, newState.filters, "json"));
  }

  getPartsForQuery(fields, filters) {
    return {
      model: this.props.model,
      fields: fields
        .map((field) => ({ asc: "+", dsc: "-", null: "" }[field.sort] + field.name))
        .join(","),
      query: filters
        .map((filter) => `${filter.name}__${filter.lookup}=${filter.value}`)
        .join("&"),
    };
  }

  getSaveUrl() {
    const parts = this.getPartsForQuery(this.state.fields, this.state.filters);
    const queryString = new URLSearchParams(parts).toString();
    return `${window.location.origin}${this.props.adminUrl}?${queryString}`;
  }

  getUrlForQuery(fields, filters, media) {
    const parts = this.getPartsForQuery(fields, filters);
    const basePath = `${this.props.baseUrl}query/${parts.model}`;
    return `${window.location.origin}${basePath}/${parts.fields}.${media}?${parts.query}`;
  }

  getUrlForMedia(media) {
    return this.getUrlForQuery(this.state.fields, this.state.filters, media);
  }

  getModelField(path) {
    const parts = path.split("__");
    const field = parts.slice(-1);
    const model = this.getFkModel(parts.slice(0, -1).join("__"));
    return this.props.allModelFields[model].fields[field];
  }

  getFieldType(path) {
    const modelField = this.getModelField(path);
    const type = modelField["type"];
    return this.props.types[type];
  }

  getFkModel(path) {
    let model = this.props.model;
    if (path) {
      for (const field of path.split("__")) {
        model = this.props.allModelFields[model].fks[field]["model"];
      }
    }
    return model;
  }

  render() {
    return (
      <Page
        config={{
          model: this.props.model,
          types: this.props.types,
          allModelFields: this.props.allModelFields,
          getUrlForMedia: this.getUrlForMedia.bind(this),
          getFkModel: this.getFkModel.bind(this),
          getFieldType: this.getFieldType.bind(this),
          getModelField: this.getModelField.bind(this),
        }}
        saveLink={this.getSaveUrl()} // todo move into query
        query={{
          addField: this.addField.bind(this),
          removeField: this.removeField.bind(this),
          toggleSort: this.toggleSort.bind(this),
          addFilter: this.addFilter.bind(this),
          removeFilter: this.removeFilter.bind(this),
          setFilterValue: this.setFilterValue.bind(this),
          setFilterLookup: this.setFilterLookup.bind(this),
        }}
        {...this.state}
      />
    );
  }
}

export default App;

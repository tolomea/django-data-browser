import React from "react";
import "./App.css";
import Page from "./Components";
const assert = require("assert");
let controller;

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      model: props.model,
      fields: props.fields,
      filters: props.filters,
      data: [],
    };
  }

  addField(path) {
    const newFields = this.state.fields.slice();
    newFields.push({ path: path, sort: null });
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
    const newSort = { asc: "dsc", dsc: null, null: "asc" }[field.sort];
    let newFields = this.state.fields.slice();

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

    this.handleQueryChange({
      fields: newFields,
    });
  }

  addFilter(path) {
    const fieldType = this.getFieldType(path);
    const newFilters = this.state.filters.slice();
    newFilters.push({
      errorMessage: null,
      path: path,
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

  setModel(model) {
    this.handleQueryChange({
      model: model,
      fields: [],
      filters: [],
      data: [],
    });
  }

  fetchData(state) {
    const url = this.getUrlForState(state, "json");

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
    const reqState = {
      model: this.state.model,
      fields: this.state.fields,
      filters: this.state.filters,
    };
    window.history.replaceState(
      reqState,
      null,
      this.getUrlForState(this.state, "html")
    );
    this.fetchData(this.state);
    window.onpopstate = (e) => {
      console.log("popstate", e.state);
      this.fetchData(e.state);
    };
  }

  handleQueryChange(queryChange) {
    const newState = { ...this.state, ...queryChange };
    this.setState(queryChange);
    const reqState = {
      model: newState.model,
      fields: newState.fields,
      filters: newState.filters,
    };
    window.history.pushState(reqState, null, this.getUrlForState(newState, "html"));
    this.fetchData(newState);
  }

  getPartsForQuery(state) {
    return {
      model: state.model,
      fields: state.fields
        .map(
          (f) =>
            f.path + { asc: `+${f.priority}`, dsc: `-${f.priority}`, null: "" }[f.sort]
        )
        .join(","),
      query: state.filters.map((f) => `${f.path}__${f.lookup}=${f.value}`).join("&"),
    };
  }

  getUrlForSave() {
    const parts = this.getPartsForQuery(this.state);
    const queryString = new URLSearchParams(parts).toString();
    return `${window.location.origin}${this.props.adminUrl}?${queryString}`;
  }

  getUrlForState(state, media) {
    const parts = this.getPartsForQuery(state);
    const basePath = `${this.props.baseUrl}query/${parts.model}`;
    return `${window.location.origin}${basePath}/${parts.fields}.${media}?${parts.query}`;
  }

  getUrlForMedia(media) {
    return this.getUrlForState(this.state, media);
  }

  getField(path) {
    const parts = path.split("__");
    const field = parts.slice(-1);
    let model = this.state.model;
    for (const field of parts.slice(0, -1)) {
      model = this.props.allModelFields[model].fks[field].model;
    }
    return this.props.allModelFields[model].fields[field];
  }

  getFieldType(path) {
    return this.props.types[this.getField(path).type];
  }

  render() {
    return (
      <Page
        config={{
          types: this.props.types,
          allModelFields: this.props.allModelFields,
          sortedModels: this.props.sortedModels,
          getFieldType: this.getFieldType.bind(this),
          getField: this.getField.bind(this),
        }}
        query={{
          addField: this.addField.bind(this),
          removeField: this.removeField.bind(this),
          toggleSort: this.toggleSort.bind(this),
          addFilter: this.addFilter.bind(this),
          removeFilter: this.removeFilter.bind(this),
          setFilterValue: this.setFilterValue.bind(this),
          setFilterLookup: this.setFilterLookup.bind(this),
          setModel: this.setModel.bind(this),
          getUrlForMedia: this.getUrlForMedia.bind(this),
          getUrlForSave: this.getUrlForSave.bind(this),
        }}
        {...this.state}
      />
    );
  }
}

export default App;

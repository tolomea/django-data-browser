import React from "react";
import "./App.css";
const assert = require("assert");

let controller;

function getAPIforWindow() {
  const location = window.location;
  const htmlUrl = location.origin + location.pathname;
  assert(htmlUrl.slice(-4) === "html");
  const jsonUrl = htmlUrl.slice(0, -4) + "json";
  return jsonUrl + location.search;
}

function Link(props) {
  return (
    <button
      type="button"
      className={"Link " + (props.className || "")}
      onClick={props.onClick}
    >
      {props.children}
    </button>
  );
}

function FilterValue(props) {
  if (props.lookup.type === "boolean")
    return (
      <select className="FilterValue" onChange={props.onChange} value={props.value}>
        <option value={true}>true</option>
        <option value={false}>false</option>
      </select>
    );
  else if (props.lookup.type === "number")
    return (
      <input
        className="FilterValue"
        type="number"
        step="0"
        name={props.name}
        value={props.value}
        onChange={props.onChange}
      />
    );
  else
    return (
      <input
        className="FilterValue"
        type="text"
        name={props.name}
        value={props.value}
        onChange={props.onChange}
      />
    );
}

class Filter extends React.Component {
  handleRemove(event) {
    const newFilters = this.props.query.filters.slice();
    newFilters.splice(this.props.index, 1);
    this.props.handleQueryChange({ filters: newFilters });
  }

  handleLookupChange(event) {
    const newFilters = this.props.query.filters.slice();
    newFilters[this.props.index] = {
      ...newFilters[this.props.index],
      lookup: event.target.value,
    };
    this.props.handleQueryChange({ filters: newFilters });
  }

  handleValueChange(event) {
    const newFilters = this.props.query.filters.slice();
    newFilters[this.props.index] = {
      ...newFilters[this.props.index],
      value: event.target.value,
    };
    this.props.handleQueryChange({ filters: newFilters });
  }

  handleAddField() {
    const newFields = this.props.query.fields.slice();
    newFields.push({
      name: this.props.name,
      sort: null,
    });
    this.props.handleQueryChange({ fields: newFields });
  }

  render() {
    const fieldType = this.props.getFieldType(this.props.name);
    return (
      <tr>
        <td>
          <Link onClick={this.handleRemove.bind(this)}>✘</Link>{" "}
          <Link onClick={this.handleAddField.bind(this)}>{this.props.name}</Link>{" "}
        </td>
        <td>
          <select
            className="Lookup"
            value={this.props.lookup}
            onChange={this.handleLookupChange.bind(this)}
          >
            {fieldType.sorted_lookups.map((lookupName) => (
              <option key={lookupName} value={lookupName}>
                {lookupName.replace("_", " ")}
              </option>
            ))}
          </select>
        </td>
        <td>=</td>
        <td>
          <FilterValue
            name={`${this.props.name}__${this.props.lookup}`}
            value={this.props.value}
            onChange={this.handleValueChange.bind(this)}
            lookup={fieldType.lookups[this.props.lookup]}
          />
          {this.props.errorMessage}
        </td>
      </tr>
    );
  }
}

function Filters(props) {
  return (
    <form className="Filters">
      <table className="Flat">
        <tbody>
          {props.query.filters.map((filter, index) => (
            <Filter
              {...filter}
              key={index}
              index={index}
              query={props.query}
              handleQueryChange={props.handleQueryChange}
              getFieldType={props.getFieldType}
            />
          ))}
        </tbody>
      </table>
    </form>
  );
}

class Toggle extends React.Component {
  constructor(props) {
    super(props);
    this.state = { isToggleOn: false };
  }

  handleClick() {
    this.setState((state) => ({
      isToggleOn: !state.isToggleOn,
    }));
  }

  render() {
    if (this.state.isToggleOn) {
      return (
        <>
          <Link className="ToggleLink" onClick={this.handleClick.bind(this)}>
            > {this.props.title}
          </Link>
          <div className="ToggleDiv">{this.props.children}</div>
        </>
      );
    } else {
      return (
        <Link className="ToggleLink" onClick={this.handleClick.bind(this)}>
          + {this.props.title}
        </Link>
      );
    }
  }
}

function Fields(props) {
  const modelFields = props.fields[props.model];
  return (
    <ul className="FieldsList">
      {modelFields.sorted_fields.map((field_name) => {
        const modelField = modelFields.fields[field_name];
        const fieldType = props.types[modelField.type];
        function handleAddFilter() {
          const newFilters = props.query.filters.slice();
          newFilters.push({
            errorMessage: null,
            name: `${props.path}${field_name}`,
            lookup: fieldType.defaultLookup,
            value:
              props.types[fieldType.lookups[fieldType.defaultLookup].type].defaultValue,
          });
          props.handleQueryChange({ filters: newFilters });
        }

        function handleAddField() {
          const newFields = props.query.fields.slice();
          newFields.push({
            name: `${props.path}${field_name}`,
            sort: null,
          });
          props.handleQueryChange({ fields: newFields });
        }

        return (
          <li key={field_name}>
            {modelField.concrete ? (
              <Link onClick={handleAddFilter}>Y</Link>
            ) : (
              <>&nbsp;&nbsp;</>
            )}{" "}
            <Link onClick={handleAddField}>{field_name}</Link>
          </li>
        );
      })}
      {modelFields.sorted_fks.map((fk_name) => {
        const fk = modelFields.fks[fk_name];
        return (
          <li key={fk_name}>
            <Toggle title={fk_name}>
              <Fields
                query={props.query}
                handleQueryChange={props.handleQueryChange}
                fields={props.fields}
                model={fk.model}
                path={`${props.path}${fk_name}__`}
                types={props.types}
              />
            </Toggle>
          </li>
        );
      })}
    </ul>
  );
}

function ResultsHead(props) {
  return (
    <thead>
      <tr>
        {props.query.fields.map((field, index) => {
          const modelField = props.getModelField(field.name);
          const fieldType = props.types[modelField.type];

          function handleRemove() {
            const newFields = props.query.fields.slice();
            newFields.splice(index, 1);
            props.handleQueryChange({
              fields: newFields,
            });
          }

          function handleAddFilter() {
            const newFilters = props.query.filters.slice();
            newFilters.push({
              errorMessage: null,
              name: field.name,
              lookup: fieldType.defaultLookup,
              value:
                props.types[fieldType.lookups[fieldType.defaultLookup].type]
                  .defaultValue,
            });
            props.handleQueryChange({
              filters: newFilters,
            });
          }

          function handleToggleSort() {
            const newFields = props.query.fields.slice();
            newFields[index] = {
              ...field,
              sort: { asc: "dsc", dsc: null, null: "asc" }[field.sort],
            };
            props.handleQueryChange({
              fields: newFields,
            });
          }

          return (
            <th key={field.name}>
              <Link onClick={handleRemove}>✘</Link>{" "}
              {modelField.concrete ? (
                <>
                  <Link onClick={handleAddFilter}>Y</Link>{" "}
                  <Link onClick={handleToggleSort}>{field.name}</Link>{" "}
                  {{ dsc: "↑", asc: "↓", null: "" }[field.sort]}
                </>
              ) : (
                field.name
              )}
            </th>
          );
        })}
        {!props.query.fields.length && <th>No fields selected</th>}
      </tr>
    </thead>
  );
}

function ResultsBody(props) {
  return (
    <tbody>
      {props.data.map((row, index) => (
        <tr key={index}>
          {row.map((cell, index) => (
            <td key={index}>{String(cell)}</td>
          ))}
        </tr>
      ))}
    </tbody>
  );
}

function Results(props) {
  return (
    <table>
      <ResultsHead
        query={props.query}
        handleQueryChange={props.handleQueryChange}
        types={props.types}
        getFieldType={props.getFieldType}
        getModelField={props.getModelField}
      />
      <ResultsBody data={props.data} />
    </table>
  );
}

function Page(props) {
  return (
    <div id="body">
      <h1>{props.model}</h1>

      <Filters
        query={props.query}
        handleQueryChange={props.handleQueryChange}
        getFieldType={props.getFieldType}
      />

      <p>
        Showing {props.data.length} results -{" "}
        <a href={props.getUrlForQuery(props.query, "csv")}>Download as CSV</a> -{" "}
        <a href={props.getUrlForQuery(props.query, "json")}>View as JSON</a> -{" "}
        <a href={props.saveLink}>Save View</a>
      </p>
      <div className="MainSpace">
        <div>
          <Fields
            query={props.query}
            handleQueryChange={props.handleQueryChange}
            fields={props.fields}
            model={props.model}
            path=""
            types={props.types}
          />
        </div>
        <Results
          query={props.query}
          handleQueryChange={props.handleQueryChange}
          data={props.data}
          types={props.types}
          getFieldType={props.getFieldType}
          getModelField={props.getModelField}
        />
      </div>
    </div>
  );
}

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      query: { filters: [], fields: [] },
    };
  }

  fetchData(url) {
    if (controller) controller.abort();
    controller = new AbortController();

    fetch(url, { signal: controller.signal })
      .then((res) => res.json())
      .then(
        (result) => {
          this.setState({
            data: result.data,
            query: { fields: result.fields, filters: result.filters },
          });
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
    const newQuery = { ...this.state.query, ...queryChange };
    this.setState({ query: newQuery });
    window.history.pushState(null, null, this.getUrlForQuery(newQuery, "html"));
    this.fetchData(this.getUrlForQuery(newQuery, "json"));
  }

  getPartsForQuery(query) {
    return {
      model: this.props.model,
      fields: query.fields
        .map((field) => ({ asc: "+", dsc: "-", null: "" }[field.sort] + field.name))
        .join(","),
      query: query.filters
        .map((filter) => `${filter.name}__${filter.lookup}=${filter.value}`)
        .join("&"),
    };
  }

  getSaveUrl(query) {
    const parts = this.getPartsForQuery(this.state.query);
    const queryString = new URLSearchParams(parts).toString();
    return `${window.location.origin}${this.props.adminUrl}?${queryString}`;
  }

  getUrlForQuery(query, media) {
    const parts = this.getPartsForQuery(query);
    const basePath = `${this.props.baseUrl}query/${parts.model}`;
    return `${window.location.origin}${basePath}/${parts.fields}.${media}?${parts.query}`;
  }

  getModelField(path) {
    const parts = path.split("__");
    const field = parts.slice(-1);
    const model = this.getFkModel(parts.slice(0, -1).join("__"));
    return this.props.fields[model].fields[field];
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
        model = this.props.fields[model].fks[field]["model"];
      }
    }
    return model;
  }

  render() {
    return (
      <Page
        data={this.state.data}
        query={this.state.query}
        handleQueryChange={this.handleQueryChange.bind(this)}
        model={this.props.model}
        saveLink={this.getSaveUrl()}
        getUrlForQuery={this.getUrlForQuery.bind(this)}
        getFkModel={this.getFkModel.bind(this)}
        getFieldType={this.getFieldType.bind(this)}
        fields={this.props.fields}
        types={this.props.types}
        getModelField={this.getModelField.bind(this)}
      />
    );
  }
}

export default App;

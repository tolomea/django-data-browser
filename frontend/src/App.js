import React from "react";
import "./App.css";
var assert = require("assert");

function getAPIforWindow() {
  const location = window.location;
  const html_url = location.origin + location.pathname;
  assert(html_url.slice(-4) === "html");
  const json_url = html_url.slice(0, -4) + "json";
  return json_url + location.search;
}

function Link(props) {
  return (
    <button
      type="button"
      className={"link " + (props.className || "")}
      onClick={props.onClick}
    >
      {props.children}
    </button>
  );
}

class Filter extends React.Component {
  handleLookupChange(event) {
    var newFilters = this.props.query.filters.slice();
    newFilters[this.props.index] = {
      ...newFilters[this.props.index],
      lookup: event.target.value,
    };
    this.props.handleQueryChange({ filters: newFilters });
  }

  getLookups() {
    const parts = this.props.filter.name.split("__");
    function follow(path, fields) {
      if (path.length > 1) {
        return follow(
          path.slice(1),
          fields.fks.find((fk) => fk.name === path[0])
        );
      } else {
        return fields.fields.find((f) => f.name === path[0]);
      }
    }
    return follow(parts, this.props.all_fields).lookups;
  }

  render() {
    return (
      <p className={this.props.filter.err_message ? "error" : undefined}>
        <Link onClick={this.props.handleRemove}>✘</Link> {this.props.filter.name}{" "}
        <select
          value={this.props.filter.lookup}
          onChange={this.handleLookupChange.bind(this)}
        >
          {this.getLookups().map((lookup) => (
            <option key={lookup} value={lookup}>
              {lookup}
            </option>
          ))}
        </select>{" "}
        ={" "}
        <input
          type="text"
          name={`${this.props.filter.name}__${this.props.filter.lookup}`}
          defaultValue={this.props.filter.value}
        />
        {this.props.filter.err_message}
      </p>
    );
  }
}

function Filters(props) {
  return (
    <form className="filters" method="get">
      {props.query.filters.map((filter, index) => (
        <Filter
          filter={filter}
          all_fields={props.all_fields} // TODO cleanup after all_fields is flattened
          key={index}
          index={index}
          query={props.query}
          handleQueryChange={props.handleQueryChange}
          handleRemove={() => {
            var newFilters = props.query.filters.slice();
            newFilters.splice(index, 1);
            props.handleQueryChange({
              filters: newFilters,
            });
          }}
        />
      ))}
      <p>
        <input type="submit" />
      </p>
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
          <Link className="toggle_link" onClick={this.handleClick.bind(this)}>
            > {this.props.title}
          </Link>
          <div className="toggle_div">{this.props.children}</div>
        </>
      );
    } else {
      return (
        <Link className="toggle_link" onClick={this.handleClick.bind(this)}>
          + {this.props.title}
        </Link>
      );
    }
  }
}

function Fields(props) {
  return (
    <ul className="fields_list">
      {props.fields.map((field) => {
        function handleAddFilter() {
          var newFilters = props.query.filters.slice();
          newFilters.push({
            err_message: null,
            name: field.name,
            lookup: "",
            value: "",
          });
          props.handleQueryChange({ filters: newFilters });
        }

        function handleAddField() {
          var newFields = props.query.fields.slice();
          newFields.push({
            name: field.name,
            sort: null,
            concrete: false,
          });
          props.handleQueryChange({ fields: newFields });
        }

        return (
          <li key={field.name}>
            {field.concrete ? (
              <Link onClick={handleAddFilter}>Y</Link>
            ) : (
              <>&nbsp;&nbsp;</>
            )}{" "}
            <Link onClick={handleAddField}>{field.name}</Link>
          </li>
        );
      })}

      {props.fks.map((fk) => (
        <li key={fk.name}>
          <Toggle title={fk.name}>
            <Fields {...fk} />
          </Toggle>
        </li>
      ))}
    </ul>
  );
}

function ResultsHead(props) {
  return (
    <thead>
      <tr>
        {props.query.fields.map((field, index) => {
          function handleRemove() {
            var newFields = props.query.fields.slice();
            newFields.splice(index, 1);
            props.handleQueryChange({
              fields: newFields,
            });
          }

          function handleAddFilter() {
            var newFilters = props.query.filters.slice();
            newFilters.push({
              err_message: null,
              name: field.name,
              lookup: "",
              value: "",
            });
            props.handleQueryChange({
              filters: newFilters,
            });
          }

          function handleToggleSort() {
            var newFields = props.query.fields.slice();
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
              {field.concrete ? (
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
            <td key={index}>{cell}</td>
          ))}
        </tr>
      ))}
    </tbody>
  );
}

function Results(props) {
  return (
    <table>
      <ResultsHead query={props.query} handleQueryChange={props.handleQueryChange} />
      <ResultsBody data={props.data} />
    </table>
  );
}

function Page(props) {
  return (
    <div id="body">
      <h1>{props.model}</h1>
      <p>
        <a href={props.csvLink}>Download as CSV</a>
      </p>
      <p>
        <a href={props.saveLink}>Save View</a>
      </p>

      <Filters
        query={props.query}
        handleQueryChange={props.handleQueryChange}
        all_fields={props.all_fields}
      />

      <p>Showing {props.data.length} results</p>
      <div className="main_space">
        <div>
          <Fields
            query={props.query}
            handleQueryChange={props.handleQueryChange}
            {...props.all_fields}
          />
        </div>
        <Results
          query={props.query}
          handleQueryChange={props.handleQueryChange}
          data={props.data}
        />
      </div>
    </div>
  );
}

class App extends React.Component {
  constructor(props) {
    super(props);
    const djangoData = JSON.parse(document.getElementById("django-data").textContent);
    this.state = {
      data: [],
      query: { filters: [], fields: [] },
      ...djangoData, // this should be props and this djangoData thing should be over in index.js
    };
  }

  fetchData(url) {
    fetch(url)
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
    window.history.pushState(null, null, this.getURLforQuery(newQuery, "html"));
    this.fetchData(this.getURLforQuery(newQuery, "json"));
  }

  getPartsForQuery(query) {
    return {
      app: this.state.app,
      model: this.state.model,
      fields: query.fields
        .map((field) => ({ asc: "+", dsc: "-", null: "" }[field.sort] + field.name))
        .join(","),
      query: query.filters
        .map((filter) => `${filter.name}__${filter.lookup}=${filter.value}`)
        .join("&"),
    };
  }

  getSaveURL(query) {
    const parts = this.getPartsForQuery(this.state.query);
    const queryString = new URLSearchParams(parts).toString();
    return `${window.location.origin}${this.state.adminURL}?${queryString}`;
  }

  getURLforQuery(query, media) {
    const parts = this.getPartsForQuery(query);
    const basePath = `${this.state.baseURL}query/${parts.app}/${parts.model}`;
    return `${window.location.origin}${basePath}/${parts.fields}.${media}?${parts.query}`;
  }

  render() {
    return (
      <Page
        data={this.state.data}
        query={this.state.query}
        all_fields={this.state.all_fields} // TODO this should be a prop
        handleQueryChange={this.handleQueryChange.bind(this)}
        model={this.state.model} // TODO this should be a prop if we need it at all
        saveLink={this.getSaveURL()}
        csvLink={this.getURLforQuery(this.state.query, "csv")}
      />
    );
  }
}

export default App;

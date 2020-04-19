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

function getBaseURL() {
  const location = window.location;
  const parts = location.pathname.split("/");
  return location.origin + parts.slice(0, -1).join("/");
}

function getURLforQuery(query, media) {
  const fieldStr = query.fields
    .map((field) => ({ asc: "+", dsc: "-", null: "" }[field.sort] + field.name))
    .join(",");
  const filterStr = query.filters
    .map((filter) => `${filter.name}__${filter.lookup}=${filter.value}`)
    .join("&");
  return `${getBaseURL()}/${fieldStr}.${media}?${filterStr}`;
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
    this.props.lookups.forEach((lookup) => {
      if (lookup.name === event.target.value) document.location.href = lookup.link;
    });
  }

  render() {
    return (
      <p className={this.props.filter.err_message ? "error" : undefined}>
        <Link onClick={this.props.handleRemove}>✘</Link> {this.props.filter.name}{" "}
        <select
          value={this.props.filter.lookup}
          onChange={this.handleLookupChange.bind(this)}
        >
          {this.props.lookups.map((lookup) => (
            <option key={lookup.name} value={lookup.name}>
              {lookup.name}
            </option>
          ))}
        </select>{" "}
        ={" "}
        <input
          type="text"
          name={`${this.props.filter.name}__${this.props.filter.lookup}`}
          value={this.props.filter.value}
        />
        {this.props.filter.err_message}
      </p>
    );
  }
}

function Filters(props) {
  return (
    <form className="filters" method="get">
      {props.lightQuery.filters.map((filter, index) => (
        <Filter
          filter={filter}
          lookups={props.query.filters[index] ? props.query.filters[index].lookups : []} // TODO cleanup after all_fields is flattened
          key={index}
          handleRemove={() => {
            var newFilters = props.lightQuery.filters.slice();
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

function AddFilter(props) {
  if (props.field.concrete) {
    return <a href={props.field.add_filter_link}>Y</a>;
  } else {
    return <>&nbsp;&nbsp;</>;
  }
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
      {props.fields.map((field) => (
        <li key={field.name}>
          <AddFilter field={field} /> <a href={field.add_link}>{field.name}</a>
        </li>
      ))}

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
          return (
            <th key={field.name}>
              <Link
                onClick={() => {
                  var newFields = props.query.fields.slice();
                  newFields.splice(index, 1);
                  props.handleQueryChange({
                    fields: newFields,
                  });
                }}
              >
                ✘
              </Link>{" "}
              {field.concrete ? (
                <>
                  <Link
                    onClick={() => {
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
                    }}
                  >
                    Y
                  </Link>{" "}
                  <Link
                    onClick={() => {
                      var newFields = props.query.fields.slice();
                      newFields[index] = {
                        ...field,
                        sort: { asc: "dsc", dsc: null, null: "asc" }[field.sort],
                      };
                      props.handleQueryChange({
                        fields: newFields,
                      });
                    }}
                  >
                    {field.name}
                  </Link>{" "}
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
      <ResultsHead
        query={props.lightQuery}
        handleQueryChange={props.handleQueryChange}
      />
      <ResultsBody data={props.data} />
    </table>
  );
}

function Page(props) {
  return (
    <div id="body">
      <h1>{props.query.model}</h1>
      <p>
        <a href={props.query.csv_link}>Download as CSV</a>
      </p>
      <p>
        <a href={props.query.save_link}>Save View</a>
      </p>

      <Filters
        query={props.query}
        lightQuery={props.lightQuery}
        handleQueryChange={props.handleQueryChange}
      />

      <p>Showing {props.data.length} results</p>
      <div className="main_space">
        <div>
          <Fields {...props.all_fields} />
        </div>
        <Results
          query={props.query}
          lightQuery={props.lightQuery}
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
    // TODO all_fileds should really be a prop and this djangoData thing should be over in index.js
    this.state = {
      data: [],
      lightQuery: { filters: [], fields: [] },
      query: djangoData.query,
      all_fields: djangoData.all_fields,
    };
  }

  fetchData(url) {
    fetch(url)
      .then((res) => res.json())
      .then(
        (result) => {
          this.setState({
            data: result.data,
            lightQuery: { fields: result.fields, filters: result.filters },
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
    const newQuery = { ...this.state.lightQuery, ...queryChange };
    window.history.pushState(null, null, getURLforQuery(newQuery, "html"));
    this.fetchData(getURLforQuery(newQuery, "json"));
  }

  render() {
    return (
      <Page
        data={this.state.data}
        lightQuery={this.state.lightQuery}
        query={this.state.query}
        all_fields={this.state.all_fields} // TODO this should be a prop
        handleQueryChange={this.handleQueryChange.bind(this)}
      />
    );
  }
}

export default App;

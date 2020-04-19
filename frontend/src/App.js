import React from "react";
import "./App.css";
var assert = require("assert");

class Filter extends React.Component {
  handleLookupChange(event) {
    this.props.filter.lookups.forEach((lookup) => {
      if (lookup.name === event.target.value) document.location.href = lookup.link;
    });
  }

  render() {
    return (
      <p className={this.props.filter.err_message ? "error" : undefined}>
        <a href={this.props.filter.remove_link}>✘</a> {this.props.filter.name}{" "}
        <select
          defaultValue={this.props.filter.lookup}
          onChange={this.handleLookupChange.bind(this)}
        >
          {this.props.filter.lookups.map((lookup) => (
            <option key={lookup.name} value={lookup.name}>
              {lookup.name}
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
    return (
      <>
        <button className="link toggle_link" onClick={this.handleClick.bind(this)}>
          + {this.props.title}
        </button>
        <div
          className="toggle_div"
          style={{ display: this.state.isToggleOn ? "block" : "none" }}
        >
          {this.props.children}
        </div>
      </>
    );
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

      <form className="filters" method="get" action={props.query.base_url}>
        {props.query.filters.map((filter, index) => (
          <Filter filter={filter} key={index} />
        ))}
        <p>
          <input type="submit" />
        </p>
        <p>Showing {props.data.length} results</p>
      </form>

      <div className="main_space">
        <div>
          <Fields {...props.query.all_fields_nested} />
        </div>
        <table>
          <thead>
            <tr>
              {props.query.fields.map((field) => {
                return (
                  <th key={field.name}>
                    <a href={field.remove_link}>✘</a>{" "}
                    {field.concrete ? (
                      <>
                        <a href={field.add_filter_link}>Y</a>{" "}
                        <a href={field.toggle_sort_link}>{field.name}</a>{" "}
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
          <tbody>
            {props.data.map((row, index) => (
              <tr key={index}>
                {row.map((cell, index) => (
                  <td key={props.query.fields[index].name}>{cell}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = { data: [] };
  }

  componentDidMount() {
    const location = window.location;
    const html_url = location.origin + location.pathname;
    assert(html_url.slice(-4) === "html");
    const json_url = html_url.slice(0, -4) + "json";

    fetch(json_url + location.search)
      .then((res) => res.json())
      .then(
        (result) => {
          this.setState({
            data: result.data,
          });
        },
        (error) => {
          this.setState({
            error,
          });
        }
      );
  }

  render() {
    const django_data = JSON.parse(document.getElementById("django-data").textContent);
    return <Page data={this.state.data} {...django_data} />;
  }
}

export default App;

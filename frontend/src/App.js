import React from "react";
import "./App.css";

function AddFilterLink(props) {
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
          <AddFilterLink field={field} /> <a href={field.add_link}>{field.name}</a>
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
          <p className={!filter.is_valid ? "error" : undefined} key={index}>
            <a href={filter.remove_link}>✘</a> {filter.name}{" "}
            <select defaultValue={filter.lookup}>
              {filter.lookups.map((lookup) => (
                <option key={lookup.name} value={lookup.name}>
                  {lookup.name}
                </option>
              ))}
            </select>{" "}
            = <input type="text" name={filter.url_name} defaultValue={filter.value} />
          </p>
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
              {props.query.sort_fields.map((sort_field) => {
                const { field, sort_icon } = sort_field;
                return (
                  <th key={field.name}>
                    <a href={field.remove_link}>✘</a>{" "}
                    {field.concrete ? (
                      <>
                        <a href={field.add_filter_link}>Y</a>{" "}
                        <a href={field.toggle_sort_link}>{field.name}</a> {sort_icon}
                      </>
                    ) : (
                      field.name
                    )}
                  </th>
                );
              })}
              {!props.query.sort_fields.length && <th>No fields selected</th>}
            </tr>
          </thead>
          <tbody>
            {props.data.map((row, index) => (
              <tr key={index}>
                {row.map((cell, index) => (
                  <td key={props.query.sort_fields[index].field.name}>{cell}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function App() {
  var django_data = JSON.parse(document.getElementById("django-data").textContent);
  return <Page {...django_data} />;
}

export default App;

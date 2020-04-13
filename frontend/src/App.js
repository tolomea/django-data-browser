import React from "react";
import "./App.css";

function AddFilterLink(props) {
  if (props.field.concrete) {
    return <a href={props.field.add_filter_link}>Y</a>;
  } else {
    return <>&nbsp;&nbsp;</>;
  }
}

function Fields(props) {
  return (
    <>
      {props.fields.map((field) => (
        <>
          <AddFilterLink field={field} />{" "}
          <a href={field.add_link}>{field.name}</a>
          <br />
        </>
      ))}

      {props.fks.map((fk) => (
        <>
          <button className="link toggle_link">+ {fk.name}</button>
          <div className="toggle_div">
            <Fields {...fk} />
          </div>
        </>
      ))}
    </>
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
        {props.query.filters.map((filter) => (
          <p className={!filter.is_valid && "error"}>
            <a href={filter.remove_link}>✘</a> {filter.name}{" "}
            <select defaultValue={filter.lookup}>
              {filter.lookups.map((lookup) => (
                <option value={lookup.name}>{lookup.name}</option>
              ))}
            </select>{" "}
            = <input type="text" name={filter.url_name} value={filter.value} />
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
          <tr>
            {props.query.sort_fields.map((sort_field) => {
              const { field, sort_icon } = sort_field;
              return (
                <th>
                  <a href={field.remove_link}>✘</a>{" "}
                  {field.concrete ? (
                    <>
                      <a href={field.add_filter_link}>Y</a>{" "}
                      <a href={field.toggle_sort_link}>{field.name}</a>{" "}
                      {sort_icon}
                    </>
                  ) : (
                    field.name
                  )}
                </th>
              );
            })}
            {!props.query.sort_fields.length && <th>No fields selected</th>}
          </tr>
          {props.data.map((row) => (
            <tr>
              {row.map((cell) => (
                <td>{cell}</td>
              ))}
            </tr>
          ))}
        </table>
      </div>
    </div>
  );
}

function App() {
  var django_data = JSON.parse(
    document.getElementById("django-data").textContent
  );
  return <Page {...django_data} />;
}

export default App;

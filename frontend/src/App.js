import React from 'react';
import './App.css';


function Fields(props) {
  return (
    <>
      {props.fields.map(field => {
        return (
          <>
            {field.concrete ? <a href={field.add_filter_link}>Y</a> : <>&nbsp;&nbsp;</>} <a href={field.add_link}>{field.name}</a>
            <br/>
          </>
        )
      })}

      {props.fks.map(fk => {
        return (
          <>
            <button className="link toggle_link">+ {fk.name}</button>
            <div class="toggle_div" id={"toggle__" + fk.path}>
              <Fields {...fk}/>
            </div>
          </>
        )
      })}

    </>
  )
}


function Page(props) {
  return (
    <div id="body">
      <h1>{props.query.model}</h1>
      <p><a href={props.query.csv_link}>Download as CSV</a></p>
      <p><a href={props.query.save_link}>Save View</a></p>

      <form className="filters" method="get" action={props.query.base_url}>
          {props.query.filters.map(filter => {
            return (
              <p className={!filter.is_valid && "error"}>
                  <a href={filter.remove_link}>✘</a> {filter.name} <select defaultValue={filter.lookup}>
                      {filter.lookups.map(lookup => { return (
                          <option value={lookup.name}>{ lookup.name }</option>
                      )})}
                  </select> = <input type="text" name={filter.url_name} value={filter.value}/>
              </p>
            )
          })}
          <p><input type="submit"/></p>
          <p>Showing {props.data.length} results</p>
      </form>

      <div className="main_space">
          <div>
              <Fields {...props.query.all_fields_nested}/>
          </div>
          <table>
              <tr>
                  {props.query.sort_fields.map(sort_field => {
                      const {field, sort_icon} = sort_field;
                      return (
                        <th>
                          <a href={field.remove_link}>✘</a>
                          {' '}
                          {field.concrete ? (
                            <>
                              <a href={field.add_filter_link}>Y</a> <a href={field.toggle_sort_link}>{field.name}</a> {sort_icon}
                            </>
                          ) : field.name }
                        </th>
                      )
                  })}
                  {!props.query.sort_fields.length && <th>No fields selected</th>}
              </tr>
              {props.data.map(row => {
                return (
                  <tr>
                      {row.map(cell => {
                        return <td>{cell}</td>
                      })}
                  </tr>
                )
              })}
          </table>
      </div>
    </div>
  );
}

function App() {
  var django_data = JSON.parse(document.getElementById('django-data').textContent);
  return (
      <Page {...django_data}/>
  );
}

export default App;

import React from "react";
import "./App.css";

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
    this.props.query.removeFilter(this.props.index);
  }

  handleLookupChange(event) {
    this.props.query.setFilterLookup(this.props.index, event.target.value);
  }

  handleValueChange(event) {
    this.props.query.setFilterValue(this.props.index, event.target.value);
  }

  handleAddField() {
    this.props.query.addField(this.props.name);
  }

  render() {
    const fieldType = this.props.config.getFieldType(this.props.name);
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
            {fieldType.sortedLookups.map((lookupName) => (
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
          {props.filters.map((filter, index) => (
            <Filter
              config={props.config}
              query={props.query}
              key={index}
              index={index}
              {...filter}
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
  const modelFields = props.config.allModelFields[props.model];
  return (
    <ul className="FieldsList">
      {modelFields.sorted_fields.map((field_name) => {
        const modelField = modelFields.fields[field_name];

        function handleAddFilter() {
          props.query.addFilter(`${props.path}${field_name}`);
        }

        function handleAddField() {
          props.query.addField(`${props.path}${field_name}`);
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
                config={props.config}
                query={props.query}
                model={fk.model}
                path={`${props.path}${fk_name}__`}
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
        {props.fields.map((field, index) => {
          const modelField = props.config.getModelField(field.name);

          function handleRemove() {
            props.query.removeField(index);
          }

          function handleAddFilter() {
            props.query.addFilter(field.name);
          }

          function handleToggleSort() {
            props.query.toggleSort(index);
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
        {!props.fields.length && <th>No fields selected</th>}
      </tr>
    </thead>
  );
}

function ResultsCell(props) {
  if (props.modelField.type === "html") {
    return <div dangerouslySetInnerHTML={{ __html: props.value }} />;
  } else return String(props.value);
}

function ResultsBody(props) {
  return (
    <tbody>
      {props.data.map((row, row_index) => (
        <tr key={row_index}>
          {row.map((cell, col_index) => (
            <td key={col_index}>
              <ResultsCell
                value={cell}
                modelField={props.config.getModelField(props.fields[col_index].name)}
              />
            </td>
          ))}
        </tr>
      ))}
    </tbody>
  );
}

function Results(props) {
  return (
    <table>
      <ResultsHead config={props.config} query={props.query} fields={props.fields} />
      <ResultsBody config={props.config} data={props.data} fields={props.fields} />
    </table>
  );
}

function Page(props) {
  return (
    <div id="body">
      <h1>{props.config.model}</h1>
      <Filters config={props.config} query={props.query} filters={props.filters} />
      <p>
        Showing {props.data.length} results -{" "}
        <a href={props.config.getUrlForMedia("csv")}>Download as CSV</a> -{" "}
        <a href={props.config.getUrlForMedia("json")}>View as JSON</a> -{" "}
        <a href={props.config.saveLink}>Save View</a>
      </p>
      <div className="MainSpace">
        <div>
          <Fields
            config={props.config}
            query={props.query}
            model={props.config.model}
            path=""
          />
        </div>
        <Results
          config={props.config}
          query={props.query}
          fields={props.fields}
          data={props.data}
        />
      </div>
    </div>
  );
}

export default Page;

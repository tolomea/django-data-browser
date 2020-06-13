import React from "react";
import "./App.css";
import { Link } from "./Util.js";
import { Results } from "./Results.js";

function FilterValue(props) {
  if (props.lookup.type === "boolean")
    return (
      <select
        className="FilterValue"
        onChange={props.onChange}
        value={props.value}
      >
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
        value={props.value}
        onChange={props.onChange}
      />
    );
  else
    return (
      <input
        className="FilterValue"
        type="text"
        value={props.value}
        onChange={props.onChange}
      />
    );
}

class Filter extends React.Component {
  render() {
    const path = this.props.path;
    const prettyPath = this.props.prettyPath;
    const index = this.props.index;
    const lookup = this.props.lookup;
    const query = this.props.query;
    const type = query.getType(query.getField(path));
    return (
      <tr>
        <td>
          <Link onClick={() => query.removeFilter(index)}>✘</Link>{" "}
          <Link onClick={() => query.addField(path, prettyPath)}>
            {prettyPath.join(" ")}
          </Link>{" "}
        </td>
        <td>
          <select
            className="Lookup"
            value={lookup}
            onChange={(e) => query.setFilterLookup(index, e.target.value)}
          >
            {type.sortedLookups.map((lookupName) => (
              <option key={lookupName} value={lookupName}>
                {lookupName.replace(/_/g, " ")}
              </option>
            ))}
          </select>
        </td>
        <td>=</td>
        <td>
          <FilterValue
            value={this.props.value}
            onChange={(e) => query.setFilterValue(index, e.target.value)}
            lookup={type.lookups[lookup]}
          />
          {this.props.errorMessage ? <p>{this.props.errorMessage}</p> : ""}
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
              query={props.query}
              key={index}
              index={index}
              {...filter}
              errorMessage={props.filterErrors[index]}
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
    return (
      <>
        <td>
          <Link className="ToggleLink" onClick={this.handleClick.bind(this)}>
            {this.state.isToggleOn ? ">" : "+"}
          </Link>
        </td>
        <td>
          {this.props.title}
          {this.state.isToggleOn && this.props.children}
        </td>
      </>
    );
  }
}

function Field(props) {
  const modelField = props.modelField;
  const title = modelField.type ? (
    <Link onClick={() => props.query.addField(props.path, props.prettyPath)}>
      {modelField.prettyName}
    </Link>
  ) : (
    modelField.prettyName
  );
  const type = props.query.getType(modelField);
  return (
    <tr>
      <td>
        {modelField.concrete && type.defaultLookup && (
          <Link
            onClick={() => props.query.addFilter(props.path, props.prettyPath)}
          >
            Y
          </Link>
        )}
      </td>

      {modelField.model ? (
        <Toggle title={title}>
          <AllFields
            query={props.query}
            model={modelField.model}
            path={props.path}
            prettyPath={props.prettyPath}
          />
        </Toggle>
      ) : (
        <>
          <td></td>
          <td>{title}</td>
        </>
      )}
    </tr>
  );
}

function AllFields(props) {
  const modelFields = props.query.getModelFields(props.model);
  return (
    <table>
      <tbody>
        {modelFields.sortedFields.map((fieldName) => {
          const modelField = modelFields.fields[fieldName];
          return (
            <Field
              key={fieldName}
              query={props.query}
              path={props.path.concat([fieldName])}
              prettyPath={props.prettyPath.concat([modelField.prettyName])}
              modelField={modelField}
            />
          );
        })}
      </tbody>
    </table>
  );
}

function ModelSelector(props) {
  return (
    <select
      className="ModelSelector"
      onChange={(e) => props.query.setModel(e.target.value)}
      value={props.model}
    >
      {props.sortedModels.map((model) => (
        <option key={model}>{model}</option>
      ))}
    </select>
  );
}

function Logo(props) {
  return (
    <div className="Logo" onClick={() => props.query.setModel("")}>
      <span>DDB</span>
      <span className="Version">v{props.version}</span>
    </div>
  );
}

function QueryPage(props) {
  const saveUrl = props.query.getUrlForSave();
  return (
    <div id="body">
      <Logo query={props.query} version={props.version} />
      <ModelSelector
        query={props.query}
        sortedModels={props.sortedModels}
        model={props.model}
      />
      <Filters
        query={props.query}
        filters={props.filters}
        filterErrors={props.filterErrors}
      />
      <p>
        Showing {props.rows.length * props.cols.length} results -{" "}
        <a href={props.query.getUrlForMedia("csv")}>Download as CSV</a> -{" "}
        <a href={props.query.getUrlForMedia("json")}>View as JSON</a>
        {saveUrl && (
          <>
            {" "}
            - <a href={saveUrl}>Save View</a>{" "}
          </>
        )}
      </p>
      <div className="MainSpace">
        <div className="FieldsList">
          <AllFields
            query={props.query}
            model={props.model}
            path={[]}
            prettyPath={[]}
          />
        </div>
        {props.query.rowFields().length || props.query.colFields().length ? (
          <Results
            query={props.query}
            rows={props.rows}
            cols={props.cols}
            body={props.body}
          />
        ) : (
          <h2>No fields selected</h2>
        )}
      </div>
    </div>
  );
}

function HomePage(props) {
  return (
    <div id="body">
      <Logo query={props.query} version={props.version} />
      <div className="Index">
        <div>
          <h1>Models</h1>
          <div>
            {props.sortedModels.map((model) => (
              <div key={model}>
                <button
                  className="Link"
                  onClick={() => props.query.setModel(model)}
                >
                  {model}
                </button>
              </div>
            ))}
          </div>
        </div>
        <div>
          <h1>Saved Views</h1>
          <div>
            {props.savedViews.map((view, index) => (
              <div key={index}>
                <button
                  className="Link"
                  onClick={() => props.query.setQuery(view.query)}
                >
                  {view.model} - {view.name}
                </button>
                <p>{view.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export { HomePage, QueryPage };

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

function RestulsFieldCell(props) {
  const modelField = props.query.getField(props.field.path);
  const type = props.query.getType(modelField);
  return (
    <th>
      <Link onClick={() => props.query.removeField(props.index)}>✘</Link>{" "}
      {modelField.concrete && type.defaultLookup ? (
        <>
          <Link
            onClick={() =>
              props.query.addFilter(props.field.path, props.field.prettyPath)
            }
          >
            Y
          </Link>{" "}
          <Link onClick={() => props.query.toggleSort(props.index)}>
            {props.field.prettyPath.join(" ")}
          </Link>{" "}
          {
            {
              dsc: `↑${props.field.priority}`,
              asc: `↓${props.field.priority}`,
              null: "",
            }[props.field.sort]
          }
        </>
      ) : (
        props.field.prettyPath.join(" ")
      )}
    </th>
  );
}

function ResultsHead(props) {
  return (
    <thead>
      <tr>
        {props.fields.map((field, index) => (
          <RestulsFieldCell
            query={props.query}
            field={field}
            index={index}
            key={index}
          />
        ))}
        {!props.fields.length && <th>No fields selected</th>}
      </tr>
    </thead>
  );
}

function ResultsCell(props) {
  return (
    <td className={props.modelField.type}>
      {props.modelField.type === "html" && props.value ? (
        <div dangerouslySetInnerHTML={{ __html: props.value }} />
      ) : (
        String(props.value)
      )}
    </td>
  );
}

function ResultsBody(props) {
  return (
    <tbody>
      {props.results.map((row, rowIndex) => (
        <tr key={rowIndex}>
          {row.map((cell, colIndex) => (
            <ResultsCell
              key={colIndex}
              query={props.query}
              value={cell}
              modelField={props.query.getField(props.fields[colIndex].path)}
            />
          ))}
        </tr>
      ))}
    </tbody>
  );
}

function Results(props) {
  return (
    <table className="Results">
      <ResultsHead query={props.query} fields={props.fields} />
      <ResultsBody
        query={props.query}
        results={props.results}
        fields={props.fields}
      />
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
        Showing {props.results.length} results -{" "}
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
        <Results
          query={props.query}
          fields={props.fields}
          results={props.results}
        />
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

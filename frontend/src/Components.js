import React, { useState } from "react";
import { Link, useParams, Redirect } from "react-router-dom";
import { TLink, SLink, doDelete, useData, version } from "./Util.js";
import { Results } from "./Results.js";
import "./App.css";

function FilterValue(props) {
  const { lookup, onChange, value } = props;
  if (props.lookup.type === "boolean")
    return (
      <select {...{ onChange, value }} className="FilterValue">
        <option value={true}>true</option>
        <option value={false}>false</option>
      </select>
    );
  else if (lookup.type === "weekday")
    return (
      <select {...{ onChange, value }} className="FilterValue">
        {[
          "Sunday",
          "Monday",
          "Tuesday",
          "Wednesday",
          "Thursday",
          "Friday",
          "Saturday",
        ].map((weekday) => (
          <option value={weekday}>{weekday}</option>
        ))}
      </select>
    );
  else if (lookup.type === "month")
    return (
      <select {...{ onChange, value }} className="FilterValue">
        {[
          "January",
          "Febuary",
          "March",
          "April",
          "May",
          "June",
          "July",
          "August",
          "September",
          "October",
          "November",
          "December",
        ].map((month) => (
          <option value={month}>{month}</option>
        ))}
      </select>
    );
  else if (lookup.type === "number" || lookup.type === "year")
    return (
      <input
        {...{ onChange, value }}
        className="FilterValue"
        type="number"
        step="0"
      />
    );
  else
    return (
      <input {...{ onChange, value }} className="FilterValue" type="text" />
    );
}

class Filter extends React.Component {
  render() {
    const {
      path,
      prettyPath,
      index,
      lookup,
      query,
      value,
      errorMessage,
    } = this.props;
    const type = query.getType(query.getField(path));
    return (
      <tr>
        <td>
          <SLink onClick={() => query.removeFilter(index)}>close</SLink>{" "}
          <TLink onClick={() => query.addField(path, prettyPath)}>
            {prettyPath.join(" ")}
          </TLink>{" "}
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
            {...{ value }}
            onChange={(e) => query.setFilterValue(index, e.target.value)}
            lookup={type.lookups[lookup]}
          />
          {errorMessage && <p>{errorMessage}</p>}
        </td>
      </tr>
    );
  }
}

function Filters(props) {
  const { query, filterErrors } = props;
  return (
    <form className="Filters">
      <table className="Flat">
        <tbody>
          {props.filters.map((filter, index) => (
            <Filter
              {...{ query, index }}
              {...filter}
              key={index}
              errorMessage={filterErrors[index]}
            />
          ))}
        </tbody>
      </table>
    </form>
  );
}

class Field extends React.Component {
  constructor(props) {
    super(props);
    this.state = { toggled: false };
  }

  toggle() {
    this.setState((state) => ({
      toggled: !state.toggled,
    }));
  }

  render() {
    const { query, path, prettyPath, modelField } = this.props;
    const type = query.getType(modelField);
    return (
      <>
        <tr>
          <td>
            {modelField.concrete && type.defaultLookup && (
              <SLink onClick={() => query.addFilter(path, prettyPath)}>
                filter_alt
              </SLink>
            )}
          </td>
          <td>
            {modelField.model && (
              <SLink className="ToggleLink" onClick={this.toggle.bind(this)}>
                {this.state.toggled ? "remove" : "add"}
              </SLink>
            )}
          </td>
          <td>
            {modelField.type ? (
              <TLink onClick={() => query.addField(path, prettyPath)}>
                {modelField.prettyName}
              </TLink>
            ) : (
              modelField.prettyName
            )}
          </td>
        </tr>
        {this.state.toggled && (
          <tr>
            <td></td>
            <td colSpan="2">
              <AllFields
                {...{ query, path, prettyPath }}
                model={modelField.model}
              />
            </td>
          </tr>
        )}
      </>
    );
  }
}

function AllFields(props) {
  const { query, model, path, prettyPath } = props;
  const modelFields = query.getModelFields(model);
  return (
    <table>
      <tbody>
        {modelFields.sortedFields.map((fieldName) => {
          const modelField = modelFields.fields[fieldName];
          return (
            <Field
              key={fieldName}
              {...{ query, modelField }}
              path={path.concat([fieldName])}
              prettyPath={prettyPath.concat([modelField.prettyName])}
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
    <Link to="/" className="Logo">
      <span>DDB</span>
      <span className="Version">v{version}</span>
    </Link>
  );
}

function QueryPage(props) {
  const {
    query,
    rows,
    cols,
    body,
    sortedModels,
    model,
    filters,
    filterErrors,
  } = props;
  const saveUrl = query.getUrlForSave();
  return (
    <>
      <ModelSelector {...{ query, sortedModels, model }} />
      <Filters {...{ query, filters, filterErrors }} />
      <p>
        Showing {rows.length * cols.length} results -{" "}
        <a href={query.getUrlForMedia("csv")}>Download as CSV</a> -{" "}
        <a href={query.getUrlForMedia("json")}>View as JSON</a>
        {saveUrl && (
          <>
            {" "}
            - <a href={saveUrl}>Save View</a>{" "}
          </>
        )}
      </p>
      <div className="MainSpace">
        <div className="FieldsList">
          <AllFields {...{ query, model }} path={[]} prettyPath={[]} />
        </div>
        {query.rowFields().length || query.colFields().length ? (
          <Results {...{ query, rows, cols, body }} />
        ) : (
          <h2>No fields selected</h2>
        )}
      </div>
    </>
  );
}

function Delete(props) {
  const [state, setState] = useState("normal");
  const { apiUrl, redirectUrl } = props;
  if (state === "normal")
    return (
      <TLink
        onClick={(event) => {
          setState("confirm");
        }}
      >
        Delete
      </TLink>
    );
  else if (state === "confirm")
    return (
      <TLink
        onClick={(event) => {
          setState("deleting");
          doDelete(apiUrl).then((response) => setState("deleted"));
        }}
      >
        Are you sure?
      </TLink>
    );
  else if (state === "deleting") return "Deleting";
  else if (state === "deleted") return <Redirect to={redirectUrl} />;
  else throw new Error(`unknown delete state: ${state}`);
}

function EditSavedView(props) {
  const { canMakePublic, baseUrl } = props;
  const { pk } = useParams();
  const url = `${baseUrl}api/views/${pk}/`;
  const [view, setView] = useData(url);
  if (!view) return "";
  return (
    <div className="EditSavedView">
      <h1>Saved View</h1>
      <form>
        <input
          type="text"
          value={view.name}
          onChange={(event) => {
            setView({ name: event.target.value });
          }}
          className="SavedViewName"
        />
        <table>
          <tbody>
            <tr>
              <th>Model:</th>
              <td>{view.model}</td>
            </tr>
            <tr>
              <th>Fields:</th>
              <td>{view.fields}</td>
            </tr>
            <tr>
              <th>Filters:</th>
              <td>{view.query}</td>
            </tr>
          </tbody>
        </table>
        <textarea
          value={view.description}
          onChange={(event) => {
            setView({ description: event.target.value });
          }}
        />
        {canMakePublic && (
          <table>
            <tbody>
              <tr>
                <th>Is Public:</th>
                <td>
                  <input
                    type="checkbox"
                    checked={view.public}
                    onChange={(event) => {
                      setView({ public: event.target.checked });
                    }}
                  />
                </td>
              </tr>
              <tr>
                <th>Public link:</th>
                <td>{view.public_link}</td>
              </tr>
              <tr>
                <th>Google Sheets:</th>
                <td>{view.google_sheets_formula}</td>
              </tr>
            </tbody>
          </table>
        )}
      </form>
      <div className="SavedViewActions">
        <Delete apiUrl={url} redirectUrl="/" />
        <Link to="/">Back</Link>
      </div>
    </div>
  );
}

function SavedViewList(props) {
  const { baseUrl } = props;
  const [savedViews] = useData(`${baseUrl}api/views/`);
  if (!savedViews) return "";
  return (
    <div>
      <h1>Saved Views</h1>
      <div>
        {savedViews.map((view, index) => (
          <div key={index}>
            <p>
              <Link className="Link" to={view.link}>
                {view.model} - {view.name}
              </Link>{" "}
              (<Link to={`/views/${view.pk}.html`}>edit</Link>)
            </p>
            <p>{view.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

function HomePage(props) {
  const { sortedModels, baseUrl } = props;
  return (
    <div className="Index">
      <div>
        <h1>Models</h1>
        <div>
          {sortedModels.map((model) => (
            <div key={model}>
              <Link to={`/query/${model}/.html`} className="Link">
                {model}
              </Link>
            </div>
          ))}
        </div>
      </div>
      <SavedViewList {...{ baseUrl }} />
    </div>
  );
}

export { HomePage, QueryPage, Logo, EditSavedView };

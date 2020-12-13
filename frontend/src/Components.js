import React, { useState } from "react";
import { Link, useParams } from "react-router-dom";
import { TLink, SLink, useData, version, Save, Delete, CopyText } from "./Util";
import { Results } from "./Results";
import { getPartsForQuery, getRelUrlForQuery } from "./Query";
import "./App.css";

function FilterValue(props) {
  const { lookupType, onChange, value, field } = props;
  const onChangeEvent = (e) => onChange(e.target.value);
  if (props.lookupType === "boolean")
    return (
      <select {...{ value }} onChange={onChangeEvent} className="FilterValue">
        <option value={true}>true</option>
        <option value={false}>false</option>
      </select>
    );
  else if (props.lookupType === "isnull")
    return (
      <select {...{ value }} onChange={onChangeEvent} className="FilterValue">
        <option value={"IsNull"}>IsNull</option>
        <option value={"NotNull"}>NotNull</option>
      </select>
    );
  else if (lookupType.endsWith("choice"))
    return (
      <select {...{ value }} onChange={onChangeEvent} className="FilterValue">
        {field.choices.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>
    );
  else if (lookupType === "number")
    return (
      <input
        {...{ value }}
        onChange={onChangeEvent}
        className="FilterValue"
        type="number"
        step="0"
      />
    );
  else if (lookupType === "jsonfield") {
    const parts = value.split(/\|(.*)/);
    return (
      <>
        <input
          value={parts[0]}
          onChange={(e) => onChange(`${e.target.value}|${parts[1]}`)}
          className="FilterValue Half"
          type="text"
        />
        <input
          value={parts[1]}
          onChange={(e) => onChange(`${parts[0]}|${e.target.value}`)}
          className="FilterValue Half"
          type="text"
        />
      </>
    );
  } else
    return (
      <input
        {...{ value }}
        onChange={onChangeEvent}
        className="FilterValue"
        type="text"
      />
    );
}

function Filter(props) {
  const { pathStr, index, lookup, query, value, errorMessage, parsed } = props;
  const field = query.getField(pathStr);
  const type = query.getType(field);
  const lookupType = type.lookups[lookup].type;
  return (
    <tr>
      <td>
        <SLink onClick={() => query.removeFilter(index)}>close</SLink>{" "}
        <TLink onClick={() => query.addField(pathStr, field.defaultSort)}>
          {query.prettyPathStr(pathStr)}
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
          {...{ value, field, lookupType }}
          onChange={(val) => query.setFilterValue(index, val)}
        />
        {errorMessage && <p className="Error">{errorMessage}</p>}
        {parsed && (lookupType == "date" || lookupType == "datetime") && (
          <p className="Success">{parsed}</p>
        )}
      </td>
    </tr>
  );
}

function Filters(props) {
  const { query, filterErrors, parsedFilterValues } = props;
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
              parsed={parsedFilterValues[index]}
            />
          ))}
        </tbody>
      </table>
    </form>
  );
}

function Field(props) {
  const { query, path, modelField } = props;
  const type = query.getType(modelField);
  const [toggled, setToggled] = useState(false);
  return (
    <>
      <tr>
        <td>
          {modelField.concrete && type.defaultLookup && (
            <SLink onClick={() => query.addFilter(path.join("__"))}>
              filter_alt
            </SLink>
          )}
        </td>
        <td>
          {modelField.model && (
            <SLink
              className="ToggleLink"
              onClick={() => setToggled((toggled) => !toggled)}
            >
              {toggled ? "remove" : "add"}
            </SLink>
          )}
        </td>
        <td>
          {modelField.type ? (
            <TLink
              onClick={() =>
                query.addField(path.join("__"), modelField.defaultSort)
              }
            >
              {modelField.prettyName}
            </TLink>
          ) : (
            modelField.prettyName
          )}
        </td>
      </tr>
      {toggled && (
        <tr>
          <td></td>
          <td colSpan="2">
            <AllFields {...{ query, path }} model={modelField.model} />
          </td>
        </tr>
      )}
    </>
  );
}

function AllFields(props) {
  const { query, model, path } = props;
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
            />
          );
        })}
      </tbody>
    </table>
  );
}

function ModelSelector(props) {
  const { query, sortedModels, model } = props;
  return (
    <select
      className="ModelSelector"
      onChange={(e) => query.setModel(e.target.value)}
      value={model}
    >
      {sortedModels.map((model) => (
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
    length,
    sortedModels,
    model,
    filters,
    filterErrors,
    parsedFilterValues,
    baseUrl,
    overlay,
    formatHints,
  } = props;

  let results;
  if (query.rowFields().length || query.colFields().length)
    results = (
      <Results {...{ query, rows, cols, body, overlay, formatHints }} />
    );
  else results = <h2>No fields selected</h2>;

  return (
    <>
      <ModelSelector {...{ query, sortedModels, model }} />
      <Filters {...{ query, filters, filterErrors, parsedFilterValues }} />
      <p>
        <span className={length >= query.query.limit ? "Error" : ""}>
          Limit:{" "}
          <input
            className="RowLimit"
            type="number"
            value={query.query.limit}
            onChange={(event) => {
              query.setLimit(event.target.value);
            }}
            min="1"
          />{" "}
          - Showing {length} results -{" "}
        </span>
        <a href={query.getUrlForMedia("csv")}>Download as CSV</a> -{" "}
        <a href={query.getUrlForMedia("json")}>View as JSON</a> -{" "}
        <a href={query.getUrlForMedia("sql")} target="_blank">View SQL Query</a> -{" "}
        <Save
          name="View"
          apiUrl={`${baseUrl}api/views/`}
          data={getPartsForQuery(query.query)}
          redirectUrl={(view) => `/views/${view.pk}.html`}
        />
      </p>
      <div className="MainSpace">
        <div className="FieldsList">
          <AllFields {...{ query, model }} path={[]} />
        </div>
        {results}
        <div />
      </div>
    </>
  );
}

function EditSavedView(props) {
  const { canMakePublic, baseUrl } = props;
  const { pk } = useParams();
  const url = `${baseUrl}api/views/${pk}/`;
  const [view, setView] = useData(url);
  if (!view) return "";
  return (
    <div className="EditSavedView">
      <div className="SavedViewActions">
        <span className="SavedViewTitle">Saved View</span>
        <Link to={view.link}>Open</Link>
      </div>
      <form>
        <input
          type="text"
          value={view.name}
          onChange={(event) => {
            setView({ name: event.target.value });
          }}
          className="SavedViewName"
          placeholder="enter a name"
        />
        <table>
          <tbody>
            <tr>
              <th>Model:</th>
              <td>{view.model}</td>
            </tr>
            <tr>
              <th>Fields:</th>
              <td>{view.fields.replace(/,/g, "\u200b,")}</td>
            </tr>
            <tr>
              <th>Filters:</th>
              <td>{view.query.replace(/&/g, "\u200b&")}</td>
            </tr>
            <tr>
              <th>Limit:</th>
              <td className="SavedViewLimit">
                <input
                  className="RowLimit"
                  type="number"
                  value={view.limit}
                  onChange={(event) => {
                    setView({ limit: event.target.value });
                  }}
                />
              </td>
            </tr>
            <tr>
              <th>Created Time:</th>
              <td>{view.createdTime}</td>
            </tr>
          </tbody>
        </table>
        <textarea
          value={view.description}
          onChange={(event) => {
            setView({ description: event.target.value });
          }}
          placeholder="enter a description"
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
                <td>{view.public && <CopyText text={view.publicLink} />}</td>
              </tr>
              <tr>
                <th>Google Sheets:</th>
                <td>
                  {view.public && <CopyText text={view.googleSheetsFormula} />}
                </td>
              </tr>
            </tbody>
          </table>
        )}
      </form>
      <div className="SavedViewActions">
        <Delete apiUrl={url} redirectUrl="/" />
        <Link to="/">Done</Link>
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
                {view.name} - {view.model}
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
  const { sortedModels, baseUrl, defaultRowLimit, allModelFields } = props;
  return (
    <div className="Index">
      <div>
        <h1>Models</h1>
        <div>
          {sortedModels.map((model) => (
            <div key={model}>
              <Link
                to={getRelUrlForQuery(
                  {
                    model: model,
                    fields: [],
                    filters: allModelFields[model].defaultFilters,
                    limit: defaultRowLimit,
                  },
                  "html"
                )}
                className="Link"
              >
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

import React, { useContext } from "react";

import { TLink, SLink, useToggle } from "./Util";
import { ShowTooltip, HideTooltip } from "./Tooltip";

import "./App.scss";

function FilterValue(props) {
  const { lookupType, onChange, value, field } = props;
  const onChangeEvent = (e) => onChange(e.target.value);
  const showTooltip = useContext(ShowTooltip);
  const hideTooltip = useContext(HideTooltip);
  const helpText = {
    date: [
      "Date filter values consist of a series of clauses applied in order left to right starting with a value of `today`.",
      "e.g. 'day=1 month+1 tuesday+2' which means move to the 1st of this month, then move forward a month, then move forward to the second Tuesday.",
      "Possible clauses include 'today', 'now' and literal date values in a variety of formats e.g. '2020-12-21'.",
      "Or you can use 'year', 'month', 'week' or 'day' with '+', '-', or '=' to add remove or replace the given quantity.",
      "Or you can use a weekday name with '+' or '-' to get the n-th next or previous (including today) instance of that day.",
      "Bear in mind that 'day=1 month+1' may produce a different result from 'month+1 day=1', for example on Jan 31st.",
    ],
    datetime: [
      "Datetime filter consist of a series of clauses applied in order left to right starting with a value of `now`.",
      "e.g. 'day=1 month+1 tuesday+2' which means move to the 1st of this month, then move forward a month, then move forward to the second Tuesday.",
      "Possible clauses include 'today', 'now' and literal date and time values in a variety of formats e.g. '2020-12-21 14:56'.",
      "Or you can use 'year', 'month', 'week', 'day', 'hour', 'minute' or 'second' with '+', '-', or '=' to add remove or replace the given quantity.",
      "Or you can use a weekday name with '+' or '-' to get the n-th next or previous (including today) instance of that day.",
      "Bear in mind that 'day=1 month+1' may produce a different result from 'month+1 day=1', for example on Jan 31st.",
    ],
  };

  if (lookupType === "boolean") {
    return (
      <select {...{ value }} onChange={onChangeEvent} className="FilterValue">
        <option value={true}>true</option>
        <option value={false}>false</option>
      </select>
    );
  } else if (lookupType === "isnull") {
    return (
      <select {...{ value }} onChange={onChangeEvent} className="FilterValue">
        <option value={"IsNull"}>IsNull</option>
        <option value={"NotNull"}>NotNull</option>
      </select>
    );
  } else if (lookupType.endsWith("choice")) {
    return (
      <select {...{ value }} onChange={onChangeEvent} className="FilterValue">
        {field.choices.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>
    );
  } else if (lookupType === "number") {
    return (
      <input
        {...{ value }}
        onChange={onChangeEvent}
        className="FilterValue"
        type="number"
        step="0"
      />
    );
  } else if (lookupType === "jsonfield") {
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
  } else {
    return (
      <input
        {...{ value }}
        onChange={onChangeEvent}
        className="FilterValue"
        type="text"
        onMouseEnter={(e) => showTooltip(e, helpText[lookupType])}
        onMouseLeave={(e) => hideTooltip(e)}
      />
    );
  }
}

function Filter(props) {
  const { pathStr, index, lookup, query, value, errorMessage, parsed } = props;
  const field = query.getField(pathStr);
  var type = null;
  var lookupType = null;
  if (field !== null) {
    type = query.getType(field);
    if (type.lookups.hasOwnProperty(lookup))
      lookupType = type.lookups[lookup].type;
  }

  if (lookupType === null)
    return (
      <tr className="Filter">
        <td>
          {" "}
          <SLink onClick={() => query.removeFilter(index)}>close</SLink>{" "}
          {pathStr}
        </td>
        <td>{lookup}</td>
        <td>=</td>
        <td>
          {value}
          <p className="Error">{errorMessage}</p>
        </td>
      </tr>
    );

  return (
    <tr className="Filter">
      <td>
        <SLink onClick={() => query.removeFilter(index)}>close</SLink>{" "}
        <TLink onClick={() => query.addField(pathStr, field.defaultSort)}>
          {query.verbosePathStr(pathStr)}
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
              {type.lookups[lookupName].verboseName}
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
        {parsed !== null &&
          (lookupType === "date" || lookupType === "datetime") && (
            <p className="Success">{parsed}</p>
          )}
      </td>
    </tr>
  );
}

function FilterList(props) {
  const { query, filters } = props;
  const [toggled, toggleLink] = useToggle(true);
  if (!filters.length) return "";
  return (
    <form className="Filters" onSubmit={(e) => e.preventDefault()}>
      <div className="FiltersToggle">{toggleLink}</div>
      {toggled && (
        <table>
          <tbody>
            {filters.map((filter, index) => (
              <Filter {...{ query, index }} {...filter} key={index} />
            ))}
          </tbody>
        </table>
      )}
    </form>
  );
}

export { FilterList };

import React from "react";
import "./App.css";
import { Link } from "./Util.js";

function Spacer(props) {
  if (props.spaces > 0) {
    return [...Array(props.spaces)].map((_, key) => (
      <td className="Empty" key={key} />
    ));
  }
  return null;
}

function HeadCell(props) {
  const modelField = props.query.getField(props.field.path);
  const type = props.query.getType(modelField);
  return (
    <th className={props.className}>
      <Link onClick={() => props.query.removeField(props.field)}>✘</Link>{" "}
      {modelField.canPivot ? (
        <>
          <Link onClick={() => props.query.togglePivot(props.field)}>
            {props.field.pivoted ? "⮦" : "⮥"}
          </Link>{" "}
        </>
      ) : (
        ""
      )}
      {modelField.concrete && type.defaultLookup ? (
        <>
          <Link
            onClick={() =>
              props.query.addFilter(props.field.path, props.field.prettyPath)
            }
          >
            Y
          </Link>{" "}
          <Link onClick={() => props.query.toggleSort(props.field)}>
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

function DataCell(props) {
  let modelField = props.query.getField(props.field.path);
  let value;
  if (props.value === undefined) {
    value = "";
  } else if (modelField.type === "html" && props.value) {
    value = <div dangerouslySetInnerHTML={{ __html: props.value }} />;
  } else {
    value = String(props.value);
  }
  return (
    <td
      className={modelField.type + " " + props.className || ""}
      colSpan={props.span || 1}
    >
      {value}
    </td>
  );
}

function VTableHeadRow(props) {
  return props.fields.map((field, i) => (
    <HeadCell
      query={props.query}
      field={field}
      index={i} // TODO remove
      key={field.pathStr}
      className={"HoriBorder " + (i ? "" : props.classNameFirst)}
    />
  ));
}

function VTableBodyRow(props) {
  return props.fields.map((field, i) => (
    <DataCell
      key={field.pathStr}
      query={props.query}
      value={props.row[field.pathStr]}
      field={field}
      className={i ? "" : props.classNameFirst}
    />
  ));
}

function HTableRow(props) {
  return (
    <>
      <HeadCell
        query={props.query}
        field={props.field}
        index={0} /* TODO remove */
      />
      {props.data.map((col, key) => (
        <DataCell
          key={key}
          query={props.query}
          value={col[props.field.pathStr]}
          field={props.field}
          span={props.span}
        />
      ))}
    </>
  );
}

function Results(props) {
  return (
    <table className="Results">
      <thead>
        <tr>
          <VTableHeadRow query={props.query} fields={props.fields} />
          {!props.fields.length && <th>No fields selected</th>}
        </tr>
      </thead>

      <tbody>
        {props.results.map((row, key) => (
          <tr key={key}>
            <VTableBodyRow
              query={props.query}
              row={row}
              fields={props.fields}
            />
          </tr>
        ))}
      </tbody>
    </table>
  );
}

function PivotResults(props) {
  return (
    <table className="Results">
      <thead>
        {/* pivoted data */}
        {props.query.colFields().map((field) => {
          return (
            <tr key={field.pathStr}>
              <Spacer spaces={props.query.rowFields().length - 1} />
              <HTableRow
                query={props.query}
                field={field}
                span={props.query.resFields().length}
                data={props.cols}
              />
            </tr>
          );
        })}

        {/* column headers */}
        <tr>
          <Spacer spaces={1 - props.query.rowFields().length} />
          <VTableHeadRow query={props.query} fields={props.query.rowFields()} />
          {props.cols.map((_, key) => (
            <VTableHeadRow
              key={key}
              query={props.query}
              fields={props.query.resFields()}
              classNameFirst="LeftBorder"
            />
          ))}
        </tr>
      </thead>

      {/* row headers and body */}
      <tbody>
        {props.rows.map((row, rowIndex) => (
          <tr key={rowIndex}>
            <Spacer spaces={1 - props.query.rowFields().length} />
            <VTableBodyRow
              query={props.query}
              fields={props.query.rowFields()}
              row={row}
            />
            {props.results.map((table, key) => (
              <VTableBodyRow
                key={key}
                query={props.query}
                fields={props.query.resFields()}
                row={table[rowIndex]}
                classNameFirst="LeftBorder"
              />
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export { Results, PivotResults };

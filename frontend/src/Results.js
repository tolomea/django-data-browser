import React from "react";
import "./App.css";
import { TLink, SLink } from "./Util";

function Spacer(props) {
  const { spaces } = props;
  if (spaces > 0) {
    return [...Array(spaces)].map((_, key) => (
      <td className="Empty" key={key} />
    ));
  }
  return null;
}

function HeadCell(props) {
  const { query, field, className } = props;
  const modelField = query.getField(field.path);
  const type = query.getType(modelField);
  return (
    <th {...{ className }}>
      <SLink onClick={() => query.removeField(field)}>close</SLink>
      {modelField.canPivot && (
        <>
          <SLink onClick={() => query.togglePivot(field)}>
            {field.pivoted ? "call_received" : "call_made"}
          </SLink>
        </>
      )}
      {modelField.concrete && type.defaultLookup ? (
        <>
          <SLink onClick={() => query.addFilter(field.path, field.prettyPath)}>
            filter_alt
          </SLink>{" "}
          <TLink onClick={() => query.toggleSort(field)}>
            {field.prettyPath.join(" ")}
            {
              {
                dsc: `↑${field.priority}`,
                asc: `↓${field.priority}`,
                null: "",
              }[field.sort]
            }
          </TLink>
        </>
      ) : (
        " " + field.prettyPath.join(" ")
      )}
    </th>
  );
}

function DataCell(props) {
  const { query, field, className, span, value } = props;
  let modelField = query.getField(field.path);
  let formattedValue;
  if (value === undefined) {
    formattedValue = "";
  } else if (modelField.type === "html" && value) {
    formattedValue = <div dangerouslySetInnerHTML={{ __html: value }} />;
  } else {
    formattedValue = String(value);
  }
  return (
    <td className={modelField.type + " " + className || ""} colSpan={span || 1}>
      {formattedValue}
    </td>
  );
}

function VTableHeadRow(props) {
  const { fields, query, classNameFirst } = props;
  return fields.map((field, i) => (
    <HeadCell
      {...{ query, field }}
      key={field.pathStr}
      className={"HoriBorder " + (i ? "" : classNameFirst)}
    />
  ));
}

function VTableBodyRow(props) {
  const { fields, query, classNameFirst, row } = props;
  return fields.map((field, i) => (
    <DataCell
      {...{ query, field }}
      key={field.pathStr}
      value={row[field.pathStr]}
      className={i ? "" : classNameFirst}
    />
  ));
}

function HTableRow(props) {
  const { query, field, data, span } = props;
  return (
    <>
      <HeadCell {...{ query, field }} />
      {data.map((col, key) => (
        <DataCell {...{ key, query, field, span }} value={col[field.pathStr]} />
      ))}
    </>
  );
}

function Results(props) {
  const { query, cols, rows, body } = props;
  return (
    <table className="Results">
      <thead>
        {/* pivoted data */}
        {query.colFields().map((field) => {
          return (
            <tr key={field.pathStr}>
              <Spacer spaces={query.rowFields().length - 1} />
              <HTableRow
                {...{ query, field }}
                span={query.resFields().length}
                data={cols}
              />
            </tr>
          );
        })}

        {/* column headers */}
        <tr>
          <Spacer spaces={1 - query.rowFields().length} />
          <VTableHeadRow {...{ query }} fields={query.rowFields()} />
          {cols.map((_, key) => (
            <VTableHeadRow
              {...{ key, query }}
              fields={query.resFields()}
              classNameFirst="LeftBorder"
            />
          ))}
        </tr>
      </thead>

      {/* row headers and body */}
      <tbody>
        {rows.map((row, rowIndex) => (
          <tr key={rowIndex}>
            <Spacer spaces={1 - query.rowFields().length} />
            <VTableBodyRow {...{ query, row }} fields={query.rowFields()} />
            {body.map((table, key) => (
              <VTableBodyRow
                {...{ key, query }}
                fields={query.resFields()}
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

export { Results };

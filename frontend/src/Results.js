import React, { useContext } from "react";
import "./App.css";
import { TLink, SLink, Overlay, syncPost } from "./Util";
import { ShowContextMenu } from "./ContextMenu";

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
  const modelField = query.getField(field.pathStr);
  const type = query.getType(modelField);

  const showContextMenu = useContext(ShowContextMenu);

  function onContextMenu(e) {
    showContextMenu(
      e,
      modelField.actions.map((action) => {
        return {
          name: action.prettyName,
          fn: () => syncPost("", { action: action.name, field: field.pathStr }),
        };
      })
    );
  }

  return (
    <th className={`HeadCell ${className}`} onContextMenu={onContextMenu}>
      <SLink onClick={() => query.removeField(field)}>close</SLink>
      <SLink onClick={() => query.moveField(field, true)}>chevron_left</SLink>
      <SLink onClick={() => query.moveField(field, false)}>chevron_right</SLink>
      {modelField.canPivot && (
        <>
          <SLink onClick={() => query.togglePivot(field)}>
            {field.pivoted ? "call_received" : "call_made"}
          </SLink>
        </>
      )}
      {modelField.concrete && type.defaultLookup ? (
        <>
          <SLink onClick={() => query.addFilter(field.pathStr)}>
            filter_alt
          </SLink>{" "}
          <TLink onClick={() => query.toggleSort(field)}>
            {query.prettyPathStr(field.pathStr)}
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
        " " + query.prettyPathStr(field.pathStr)
      )}
    </th>
  );
}

function DataCell(props) {
  const {
    modelField,
    className,
    span,
    value,
    formatHint,
    query,
    pathStr,
    fullRow,
  } = props;
  let formattedValue;
  if (value === undefined) {
    formattedValue = "";
  } else if (value === null) {
    formattedValue = null;
  } else if (modelField.type === "html") {
    formattedValue = value;
  } else if (modelField.type === "number") {
    if (
      value > formatHint.highCutOff ||
      value < -formatHint.highCutOff ||
      (value && value < formatHint.lowCutOff && value > -formatHint.lowCutOff)
    ) {
      formattedValue = value.toExponential(formatHint.significantFigures - 1);
    } else {
      formattedValue = value.toLocaleString(undefined, formatHint);
    }
  } else {
    formattedValue = String(value);
  }

  const showContextMenu = useContext(ShowContextMenu);

  function onContextMenu(e) {
    showContextMenu(e, [
      navigator.clipboard && {
        name: "Copy",
        fn: () => navigator.clipboard.writeText(formattedValue),
      },
      modelField.concrete &&
        query.getType(modelField).lookups.hasOwnProperty("equals") && {
          name: "Filter",
          fn: () => query.addExactFilter(pathStr, value),
        },
      fullRow && {
        name: "Drill down",
        fn: () => query.drillDown(fullRow),
      },
    ]);
  }

  return (
    <td
      className={`DataCell ${modelField.type + " " + className || ""}`}
      colSpan={span || 1}
      onContextMenu={onContextMenu}
    >
      {modelField.type === "html" ? (
        <div dangerouslySetInnerHTML={{ __html: value }} />
      ) : (
        formattedValue
      )}
    </td>
  );
}

function VTableHeadRow(props) {
  const { fields, query, classNameFirst, className } = props;
  return fields.map((field, i) => (
    <HeadCell
      {...{ query, field }}
      key={field.pathStr}
      className={`HoriBorder ${className} ` + (i ? "" : classNameFirst)}
    />
  ));
}

function VTableBodyRow(props) {
  const {
    fields,
    query,
    classNameFirst,
    className,
    row,
    formatHints,
    fullRow,
  } = props;
  return fields.map((field, i) => {
    if (row)
      return (
        <DataCell
          {...{ query }}
          pathStr={field.pathStr}
          key={field.pathStr}
          value={row[field.pathStr]}
          className={`${i ? "" : classNameFirst} ${className}`}
          modelField={query.getField(field.pathStr)}
          formatHint={formatHints[field.pathStr]}
          fullRow={fullRow}
        />
      );
    else
      return (
        <td
          key={field.pathStr}
          className={`${i ? "" : classNameFirst} Empty`}
        ></td>
      );
  });
}

function HTableRow(props) {
  const { query, field, data, span, className, formatHints } = props;
  return (
    <>
      <HeadCell {...{ query, field }} />
      {data.map((col, key) => (
        <DataCell
          {...{ key, span, className, query }}
          value={col[field.pathStr]}
          modelField={query.getField(field.pathStr)}
          formatHint={formatHints[field.pathStr]}
          fullRow={col}
          pathStr={field.pathStr}
        />
      ))}
    </>
  );
}

function Results(props) {
  const { query, cols, rows, body, overlay, formatHints } = props;
  return (
    <div className="Results">
      <Overlay message={overlay} />
      <div className="Scroller">
        <table>
          <thead>
            {/* pivoted data */}
            {query.colFields().map((field) => {
              return (
                <tr key={field.pathStr}>
                  <Spacer spaces={query.rowFields().length - 1} />
                  <HTableRow
                    {...{ query, field, formatHints }}
                    span={query.resFields().length}
                    data={cols}
                    className={overlay && "Fade"}
                  />
                </tr>
              );
            })}

            {/* column headers */}
            <tr>
              <Spacer spaces={1 - query.rowFields().length} />
              <VTableHeadRow
                {...{ query }}
                fields={query.rowFields()}
                className="Freeze"
              />
              {cols.map((_, key) => (
                <VTableHeadRow
                  {...{ key, query }}
                  fields={query.resFields()}
                  classNameFirst="LeftBorder"
                  className="Freeze"
                />
              ))}
            </tr>
          </thead>

          {/* row headers and body */}
          <tbody className={overlay && "Fade"}>
            {rows.map((row, rowIndex) => (
              <tr key={rowIndex}>
                <Spacer spaces={1 - query.rowFields().length} />
                <VTableBodyRow
                  {...{ query, row, formatHints }}
                  fields={query.rowFields()}
                  fullRow={row}
                />
                {body.map((table, key) => (
                  <VTableBodyRow
                    {...{ key, query, formatHints }}
                    fields={query.resFields()}
                    row={table[rowIndex]}
                    fullRow={{ ...row, ...cols[key] }}
                    classNameFirst="LeftBorder"
                  />
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export { Results };

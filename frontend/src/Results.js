import React, { useContext } from "react";
import "./App.css";
import { TLink, SLink, Overlay, syncPost, doPost, HasActionIcon } from "./Util";
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
  const {
    query,
    field,
    className,
    leftArrow,
    rightArrow,
    verticalArrows,
  } = props;
  const modelField = query.getField(field.pathStr);
  const type = query.getType(modelField);
  const fieldClass = query.getFieldClass(modelField);

  const showContextMenu = useContext(ShowContextMenu);

  function onContextMenu(e) {
    showContextMenu(
      e,
      modelField.actions.map((action) => {
        return {
          name: action.prettyName,
          fn: () =>
            doPost("", {
              action: action.name,
              field: field.pathStr,
            }).then((response) => syncPost(response.url, response.data)),
        };
      })
    );
  }

  return (
    <th
      className={`HeadCell ContextCursor ${className} ${fieldClass}`}
      onContextMenu={onContextMenu}
    >
      <SLink onClick={() => query.removeField(field)}>close</SLink>
      {leftArrow && (
        <SLink onClick={() => query.moveField(field, true)}>
          {verticalArrows ? "expand_less" : "chevron_left"}
        </SLink>
      )}
      {rightArrow && (
        <SLink onClick={() => query.moveField(field, false)}>
          {verticalArrows ? "expand_more" : "chevron_right"}
        </SLink>
      )}
      {modelField.canPivot && (
        <SLink onClick={() => query.togglePivot(field)}>
          pivot_table_chart
        </SLink>
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
      <HasActionIcon
        modelField={modelField}
        message="Admin actions availble on right click."
      />
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

  // The value we will use in copy
  let formattedValue;
  if (value === undefined) {
    formattedValue = "";
  } else if (value === null) {
    formattedValue = "null";
  } else if (modelField.type === "html") {
    formattedValue = value;
  } else if (modelField.type === "url") {
    formattedValue = <a href={value}>{value}</a>;
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

  // Any extra gubbins we need to render it
  let displayValue;
  if (value === null) {
    displayValue = <span className="Null">{formattedValue}</span>;
  } else if (formattedValue === "") {
    displayValue = "\xa0"; // nbsp
  } else if (modelField.type === "html") {
    displayValue = <div dangerouslySetInnerHTML={{ __html: value }} />;
  } else {
    displayValue = formattedValue;
  }

  const showContextMenu = useContext(ShowContextMenu);
  function onContextMenu(e) {
    modelField.type !== "html" &&
      showContextMenu(e, [
        navigator.clipboard && {
          name: "Copy",
          fn: () => navigator.clipboard.writeText(formattedValue),
        },
        modelField.concrete &&
          query.filterForValue(pathStr, value) && {
            name: "Filter",
            fn: () => query.addExactFilter(pathStr, value),
          },
        modelField.concrete &&
          query.filterForValue(pathStr, value) && {
            name: "Exclude",
            fn: () => query.addExactExclude(pathStr, value),
          },
        fullRow && {
          name: "Drill down",
          fn: () => query.drillDown(fullRow),
        },
      ]);
  }

  return (
    <td
      className={`DataCell ContextCursor ${modelField.type} ${className}`}
      colSpan={span || 1}
      onContextMenu={onContextMenu}
    >
      {displayValue}
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
      verticalArrows={false}
      leftArrow={i !== 0}
      rightArrow={i !== fields.length - 1}
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
  const {
    query,
    field,
    data,
    span,
    className,
    formatHints,
    leftArrow,
    rightArrow,
  } = props;
  return (
    <>
      <HeadCell
        {...{ query, field, leftArrow, rightArrow }}
        verticalArrows={true}
      />
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
  const colFields = query.colFields();
  const topTitleSpace = query.rowFields().length - 1;
  const sideTitleSpace = query.colFields().length
    ? 1 - query.rowFields().length
    : 0;
  const hasBody = query.rowFields().length || query.bodyFields().length || null;

  return (
    <div className="Results">
      <Overlay message={overlay} />
      <div className="Scroller">
        <table>
          <thead>
            {/* col headers and data aka pivots */}
            {colFields.map((field, i) => {
              return (
                <tr key={field.pathStr}>
                  <Spacer spaces={topTitleSpace} />
                  <HTableRow
                    {...{ query, field, formatHints }}
                    span={query.bodyFields().length}
                    data={cols}
                    className={overlay && "Fade"}
                    leftArrow={i !== 0}
                    rightArrow={i !== colFields.length - 1}
                  />
                </tr>
              );
            })}

            {/* body/aggregate headers */}
            {hasBody && (
              <tr>
                <Spacer spaces={sideTitleSpace} />
                <VTableHeadRow
                  {...{ query }}
                  fields={query.rowFields()}
                  className="Freeze"
                />
                {(cols.length ? cols : [null]).map((_, key) => (
                  <VTableHeadRow
                    {...{ key, query }}
                    fields={query.bodyFields()}
                    classNameFirst="LeftBorder"
                    className="Freeze"
                  />
                ))}
              </tr>
            )}
          </thead>

          {/* row headers and body */}
          <tbody className={overlay && "Fade"}>
            {hasBody &&
              rows.map(
                (row, rowIndex) =>
                  row && (
                    <tr key={rowIndex}>
                      <Spacer spaces={sideTitleSpace} />
                      <VTableBodyRow
                        {...{ query, row, formatHints }}
                        fields={query.rowFields()}
                        fullRow={row}
                      />
                      {body.map((table, key) => (
                        <VTableBodyRow
                          {...{ key, query, formatHints }}
                          fields={query.bodyFields()}
                          row={table[rowIndex]}
                          fullRow={{ ...row, ...cols[key] }}
                          classNameFirst="LeftBorder"
                        />
                      ))}
                    </tr>
                  )
              )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export { Results };

import React from "react";
import "./App.css";
import { Link } from "./Util.js";

function ResultsFieldCell(props) {
  const modelField = props.query.getField(props.field.path);
  const type = props.query.getType(modelField);
  return (
    <th className={props.className}>
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
          <ResultsFieldCell
            query={props.query}
            field={field}
            index={index}
            key={index}
            className={"HoriBorder"}
          />
        ))}
        {!props.fields.length && <th>No fields selected</th>}
      </tr>
    </thead>
  );
}

function ResultsCell(props) {
  let value;
  if (props.value === undefined) {
    value = "";
  } else if (props.modelField.type === "html" && props.value) {
    value = <div dangerouslySetInnerHTML={{ __html: props.value }} />;
  } else {
    value = String(props.value);
  }
  return (
    <td
      className={props.modelField.type + " " + props.className || ""}
      colSpan={props.span || 1}
    >
      {value}
    </td>
  );
}

function ResultsBody(props) {
  return (
    <tbody>
      {props.results.map((row, rowIndex) => (
        <tr key={rowIndex}>
          {props.fields.map((field, colIndex) => (
            <ResultsCell
              key={colIndex}
              query={props.query}
              value={row[field.pathStr]}
              modelField={props.query.getField(field.path)}
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

function PivotResults(props) {
  const colFields = props.fields.filter((f) => f.pivoted);
  const rowFields = props.fields.filter(
    (f) => !f.pivoted && props.query.getField(f.path).canPivot
  );
  const resFields = props.fields.filter(
    (f) => !props.query.getField(f.path).canPivot
  );
  return (
    <table className="Results">
      <thead>
        {/* col headers */}
        {colFields.map((field, index) => {
          return (
            <tr key={index}>
              {[...Array(rowFields.length ? rowFields.length - 1 : 0)].map(
                () => (
                  <td className="Empty" />
                )
              )}
              <ResultsFieldCell
                query={props.query}
                field={field}
                index={0} /* TODO how are we going to get this? */
              />
              {props.cols.map((cells) => (
                <ResultsCell
                  query={props.query}
                  value={cells[field.pathStr]}
                  modelField={props.query.getField(field.path)}
                  span={resFields.length}
                  className="SoftLeftBorder"
                />
              ))}
            </tr>
          );
        })}

        {/* res headers */}
        <tr>
          {rowFields.length ? undefined : <td className="Empty" />}
          {rowFields.map((field) => (
            <ResultsFieldCell
              query={props.query}
              field={field}
              index={0} /* TODO how are we going to get this? */
              className="HoriBorder"
            />
          ))}
          {props.cols.map(() =>
            resFields.map((field, index) => (
              <ResultsFieldCell
                query={props.query}
                field={field}
                index={0} /* TODO how are we going to get this? */
                className={"HoriBorder" + (index ? "" : " LeftBorder")}
              />
            ))
          )}
        </tr>
      </thead>
      <tbody>
        {props.rows.map((row, index) => (
          <tr>
            {/* row headers */}
            {rowFields.length ? undefined : <td className="Empty" />}
            {rowFields.map((field) => (
              <ResultsCell
                query={props.query}
                value={row[field.pathStr]}
                modelField={props.query.getField(field.path)}
              />
            ))}
            {/* results */}
            {props.results[index].map((row) =>
              resFields.map((field, i) => (
                <ResultsCell
                  query={props.query}
                  value={row[field.pathStr]}
                  modelField={props.query.getField(field.path)}
                  className={i ? "" : "LeftBorder"}
                />
              ))
            )}
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export { Results, PivotResults };

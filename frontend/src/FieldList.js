import {
  TLink,
  SLink,
  HasActionIcon,
  HasToManyIcon,
  useToggle,
  strMatch,
} from "./Util";

import "./App.scss";

function Field(props) {
  const { query, path, modelField, fieldFilter } = props;
  const type = query.getType(modelField);
  const [toggled, toggleLink] = useToggle();
  const expanded = modelField.model && (toggled || fieldFilter);

  return (
    <>
      <tr className="Field">
        {/* filter */}
        <td>
          {modelField.concrete && type.defaultLookup && (
            <SLink onClick={() => query.addFilter(path.join("__"))}>
              filter_alt
            </SLink>
          )}
        </td>

        {/* expand */}
        <td>{modelField.model && toggleLink}</td>

        {/* name */}
        <td className={`FieldName ${query.getFieldClass(modelField)}`}>
          {modelField.type ? (
            <TLink
              onClick={() =>
                query.addField(path.join("__"), modelField.defaultSort)
              }
            >
              {modelField.verboseName}
              <HasActionIcon
                modelField={modelField}
                message="Has admin actions."
              />
            </TLink>
          ) : (
            <>
              {modelField.verboseName}
              <HasToManyIcon
                modelField={modelField}
                message="Traversing 'To Many' links may add multiple lines per result."
              />
            </>
          )}
        </td>
      </tr>

      {/* sub fields */}
      {expanded && (
        <tr>
          <td></td>
          <td colSpan="2">
            <FieldGroup
              {...{ query, path, fieldFilter }}
              model={modelField.model}
            />
          </td>
        </tr>
      )}
    </>
  );
}

function FieldGroup(props) {
  const { query, model, path, fieldFilter } = props;
  const modelFields = query.getModelFields(model);
  const filterParts = fieldFilter.toLowerCase().split(".");
  return (
    <table className="FieldGroup">
      <tbody>
        {modelFields.sortedFields.map((fieldName) => {
          const modelField = modelFields.fields[fieldName];
          if (!strMatch(filterParts[0], modelField.verboseName.toLowerCase()))
            return null;
          return (
            <Field
              key={fieldName}
              {...{ query, modelField }}
              path={path.concat([fieldName])}
              fieldFilter={filterParts.slice(1).join(".")}
            />
          );
        })}
      </tbody>
    </table>
  );
}

function FieldList(props) {
  const { query, model, fieldFilter } = props;

  return (
    <div className="Scroller">
      <FieldGroup {...{ query, model, fieldFilter }} path={[]} />
    </div>
  );
}

export { FieldList };

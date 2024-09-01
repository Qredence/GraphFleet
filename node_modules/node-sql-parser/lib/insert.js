(function (global, factory) {
  if (typeof define === "function" && define.amd) {
    define(["exports", "./tables", "./expr", "./column", "./util", "./select", "./update"], factory);
  } else if (typeof exports !== "undefined") {
    factory(exports, require("./tables"), require("./expr"), require("./column"), require("./util"), require("./select"), require("./update"));
  } else {
    var mod = {
      exports: {}
    };
    factory(mod.exports, global.tables, global.expr, global.column, global.util, global.select, global.update);
    global.insert = mod.exports;
  }
})(typeof globalThis !== "undefined" ? globalThis : typeof self !== "undefined" ? self : this, function (_exports, _tables, _expr, _column, _util, _select, _update) {
  "use strict";

  Object.defineProperty(_exports, "__esModule", {
    value: true
  });
  _exports.conflictToSQL = conflictToSQL;
  _exports.insertToSQL = insertToSQL;
  _exports.valuesToSQL = valuesToSQL;
  /**
   * @param {Array} values
   * @return {string}
   */
  function valuesToSQL(values) {
    if (values.type === 'select') return (0, _select.selectToSQL)(values);
    const clauses = values.map(_expr.exprToSQL);
    return `(${clauses.join('), (')})`;
  }
  function partitionToSQL(partition) {
    if (!partition) return '';
    const partitionArr = ['PARTITION', '('];
    if (Array.isArray(partition)) {
      partitionArr.push(partition.map(_util.identifierToSql).join(', '));
    } else {
      const {
        value
      } = partition;
      partitionArr.push(value.map(_expr.exprToSQL).join(', '));
    }
    partitionArr.push(')');
    return partitionArr.filter(_util.hasVal).join('');
  }
  function conflictTargetToSQL(conflictTarget) {
    if (!conflictTarget) return '';
    const {
      type
    } = conflictTarget;
    switch (type) {
      case 'column':
        return `(${conflictTarget.expr.map(_column.columnRefToSQL).join(', ')})`;
    }
  }
  function conflictActionToSQL(conflictAction) {
    const {
      expr,
      keyword
    } = conflictAction;
    const {
      type
    } = expr;
    const result = [(0, _util.toUpper)(keyword)];
    switch (type) {
      case 'origin':
        result.push((0, _util.literalToSQL)(expr));
        break;
      case 'update':
        result.push('UPDATE', (0, _util.commonOptionConnector)('SET', _update.setToSQL, expr.set), (0, _util.commonOptionConnector)('WHERE', _expr.exprToSQL, expr.where));
        break;
    }
    return result.filter(_util.hasVal).join(' ');
  }
  function conflictToSQL(conflict) {
    if (!conflict) return '';
    const {
      action,
      target
    } = conflict;
    const result = [conflictTargetToSQL(target), conflictActionToSQL(action)];
    return result.filter(_util.hasVal).join(' ');
  }
  function insertToSQL(stmt) {
    const {
      table,
      type,
      prefix = 'into',
      columns,
      conflict,
      values,
      where,
      on_duplicate_update: onDuplicateUpdate,
      partition,
      returning,
      set
    } = stmt;
    const {
      keyword,
      set: duplicateSet
    } = onDuplicateUpdate || {};
    const clauses = [(0, _util.toUpper)(type), (0, _util.toUpper)(prefix), (0, _tables.tablesToSQL)(table), partitionToSQL(partition)];
    if (Array.isArray(columns)) clauses.push(`(${columns.map(_util.literalToSQL).join(', ')})`);
    clauses.push((0, _util.commonOptionConnector)(Array.isArray(values) ? 'VALUES' : '', valuesToSQL, values));
    clauses.push((0, _util.commonOptionConnector)('ON CONFLICT', conflictToSQL, conflict));
    clauses.push((0, _util.commonOptionConnector)('SET', _update.setToSQL, set));
    clauses.push((0, _util.commonOptionConnector)('WHERE', _expr.exprToSQL, where));
    clauses.push((0, _util.returningToSQL)(returning));
    clauses.push((0, _util.commonOptionConnector)(keyword, _update.setToSQL, duplicateSet));
    return clauses.filter(_util.hasVal).join(' ');
  }
});
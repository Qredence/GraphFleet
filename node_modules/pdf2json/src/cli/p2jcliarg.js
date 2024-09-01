"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.yargs = exports.CLIArgParser = void 0;
var pdfparser_js_1 = require("../../dist/pdfparser.js");
var pkInfo = pdfparser_js_1.default.pkInfo, _PRO_TIMER = pdfparser_js_1.default._PARSER_SIG;
var CLIArgParser = /** @class */ (function () {
    // constructor
    function CLIArgParser(args) {
        this.args = [];
        this.aliases = {};
        this.usageMsg = ""; // Rename 'usage' to 'usageMsg'
        this.parsedArgv = null;
        if (Array.isArray(args))
            this.args = args;
    }
    CLIArgParser.prototype.usage = function (usageMsg) {
        this.usageMsg = "".concat(usageMsg, "\n\nOptions:\n"); // Rename 'usage' to 'usageMsg'
        return this;
    };
    CLIArgParser.prototype.alias = function (key, name, description) {
        this.aliases[key] = { name: name, description: description };
        return this;
    };
    CLIArgParser.prototype.showHelp = function () {
        var helpMsg = this.usageMsg;
        for (var _i = 0, _a = Object.entries(this.aliases); _i < _a.length; _i++) {
            var _b = _a[_i], key = _b[0], value = _b[1];
            var name_1 = value.name, description = value.description;
            helpMsg += "-".concat(key, ",--").concat(name_1, "\t ").concat(description, "\n");
        }
        console.log(helpMsg);
    };
    Object.defineProperty(CLIArgParser.prototype, "argv", {
        get: function () {
            return this.parsedArgv ? this.parsedArgv : this.parseArgv();
        },
        enumerable: false,
        configurable: true
    });
    CLIArgParser.isNumber = function (x) {
        if (typeof x === "number")
            return true;
        if (/^0x[0-9a-f]+$/i.test(x))
            return true;
        return /^[-+]?(?:\d+(?:\.\d*)?|\.\d+)(e[-+]?\d+)?$/.test(x);
    };
    CLIArgParser.prototype.setArg = function (key, val, argv) {
        var _this = this;
        var value = CLIArgParser.isNumber(val) ? Number(val) : val;
        this.setKey(argv, key.split("."), value);
        var aliasKey = key in this.aliases ? [this.aliases[key].name] : [];
        if (aliasKey.length < 1) {
            for (var _i = 0, _a = Object.entries(this.aliases); _i < _a.length; _i++) {
                var _b = _a[_i], akey = _b[0], avalue = _b[1];
                if (key === avalue.name) {
                    aliasKey.push(akey);
                    break;
                }
            }
        }
        aliasKey.forEach(function (x) { return _this.setKey(argv, x.split("."), value); });
    };
    CLIArgParser.prototype.setKey = function (obj, keys, value) {
        var o = obj;
        for (var i = 0; i < keys.length - 1; i++) {
            var key_1 = keys[i];
            if (key_1 === "__proto__")
                return;
            if (o[key_1] === undefined)
                o[key_1] = {};
            if (o[key_1] === Object.prototype ||
                o[key_1] === Number.prototype ||
                o[key_1] === String.prototype)
                o[key_1] = {};
            if (o[key_1] === Array.prototype)
                o[key_1] = [];
            o = o[key_1];
        }
        var key = keys[keys.length - 1];
        if (key === "__proto__")
            return;
        if (o === Object.prototype ||
            o === Number.prototype ||
            o === String.prototype)
            o = {};
        if (o === Array.prototype)
            o = [];
        if (o[key] === undefined) {
            o[key] = value;
        }
        else if (Array.isArray(o[key])) {
            o[key].push(value);
        }
        else {
            o[key] = [o[key], value];
        }
    };
    CLIArgParser.prototype.parseArgv = function () {
        var args = this.args; // aliases = this.#aliases,
        var argv = {};
        for (var i = 0; i < args.length; i++) {
            var arg = args[i];
            if (/^--.+/.test(arg)) {
                var extractKey = arg.match(/^--(.+)/);
                if (!Array.isArray(extractKey)) {
                    console.warn("Unknow CLI options:", arg);
                    continue; // continue if no match
                }
                var key = extractKey[1];
                var next = args[i + 1];
                if (next !== undefined && !/^-/.test(next)) {
                    this.setArg(key, next, argv);
                    i++;
                }
                else if (/^(true|false)$/.test(next)) {
                    this.setArg(key, next === "true", argv);
                    i++;
                }
                else {
                    this.setArg(key, true, argv);
                }
            }
            else if (/^-[^-]+/.test(arg)) {
                var key = arg.slice(-1)[0];
                if (key !== "-") {
                    if (args[i + 1] && !/^(-|--)[^-]/.test(args[i + 1])) {
                        this.setArg(key, args[i + 1], argv);
                        i++;
                    }
                    else if (args[i + 1] && /^(true|false)$/.test(args[i + 1])) {
                        this.setArg(key, args[i + 1] === "true", argv);
                        i++;
                    }
                    else {
                        this.setArg(key, true, argv);
                    }
                }
            }
            else {
                console.warn("Unknow CLI options:", arg);
            }
        }
        this.parsedArgv = argv;
        return argv;
    };
    return CLIArgParser;
}());
exports.CLIArgParser = CLIArgParser;
exports.yargs = new CLIArgParser(process.argv.slice(2))
    .usage("\n".concat(_PRO_TIMER, "\n\nUsage: ").concat(pkInfo.name, " -f|--file [-o|output_dir]"))
    .alias("v", "version", "Display version.")
    .alias("h", "help", "Display brief help information.")
    .alias("f", "file", "(required) Full path of input PDF file or a directory to scan for all PDF files.\n\t\t When specifying a PDF file name, it must end with .PDF, otherwise it would be treated as a input directory.")
    .alias("o", "output", "(optional) Full path of output directory, must already exist.\n\t\t Current JSON file in the output folder will be replaced when file name is same.")
    .alias("s", "silent", "(optional) when specified, will only log errors, otherwise verbose.")
    .alias("t", "fieldTypes", "(optional) when specified, will generate .fields.json that includes fields ids and types.")
    .alias("c", "content", "(optional) when specified, will generate .content.txt that includes text content from PDF.")
    .alias("m", "merge", "(optional) when specified, will generate .merged.json that includes auto-merged broken text blocks from PDF.")
    .alias("r", "stream", "(optional) when specified, will process and parse with buffer/object transform stream rather than file system.");

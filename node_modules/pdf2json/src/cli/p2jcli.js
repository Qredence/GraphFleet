"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (g && (g = 0, op[0] && (_ = 0)), _) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
Object.defineProperty(exports, "__esModule", { value: true });
var nodeUtil = require("util");
var fs = require("fs");
var path_1 = require("path");
var p2jcliarg_js_1 = require("./p2jcliarg.js");
var pdfparser_js_1 = require("../../dist/pdfparser.js");
var ParserStream = pdfparser_js_1.default.ParserStream, StringifyStream = pdfparser_js_1.default.StringifyStream, pkInfo = pdfparser_js_1.default.pkInfo, _PRO_TIMER = pdfparser_js_1.default._PARSER_SIG;
var argv = p2jcliarg_js_1.yargs.argv;
var ONLY_SHOW_VERSION = "v" in argv;
var ONLY_SHOW_HELP = "h" in argv;
var VERBOSITY_LEVEL = "s" in argv ? 0 : 5;
var HAS_INPUT_DIR_OR_FILE = "f" in argv;
var PROCESS_RAW_TEXT_CONTENT = "c" in argv;
var PROCESS_FIELDS_CONTENT = "t" in argv;
var PROCESS_MERGE_BROKEN_TEXT_BLOCKS = "m" in argv;
var PROCESS_WITH_STREAM = "r" in argv;
var INPUT_DIR_OR_FILE = argv.f;
var PDFProcessor = /** @class */ (function () {
    // constructor
    function PDFProcessor(inputDir, inputFile, curCLI) {
        this.inputDir = '';
        this.inputFile = '';
        this.inputPath = '';
        this.outputDir = '';
        this.outputFile = '';
        this.outputPath = '';
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        this.pdfParser = null;
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        this.curCLI = null;
        this.getOutputFile = function () {
            return path_1.default.join(this.outputDir, this.outputFile);
        };
        // public, this instance copies
        this.inputDir = path_1.default.normalize(inputDir);
        this.inputFile = inputFile;
        this.inputPath = path_1.default.join(this.inputDir, this.inputFile);
        this.outputDir = path_1.default.normalize(argv.o || inputDir);
        this.pdfParser = null;
        this.curCLI = curCLI;
    }
    //private methods
    PDFProcessor.prototype.generateMergedTextBlocksStream = function () {
        var _this = this;
        return new Promise(function (resolve, reject) {
            if (!_this.pdfParser) {
                reject("PDFParser instance is not available.");
                return;
            }
            var outputStream = ParserStream.createOutputStream(_this.outputPath.replace(".json", ".merged.json"), resolve, reject);
            _this.pdfParser
                .getMergedTextBlocksStream()
                .pipe(new StringifyStream())
                .pipe(outputStream);
        });
    };
    PDFProcessor.prototype.generateRawTextContentStream = function () {
        var _this = this;
        return new Promise(function (resolve, reject) {
            var outputStream = ParserStream.createOutputStream(_this.outputPath.replace(".json", ".content.txt"), resolve, reject);
            _this.pdfParser.getRawTextContentStream().pipe(outputStream);
        });
    };
    PDFProcessor.prototype.generateFieldsTypesStream = function () {
        var _this = this;
        return new Promise(function (resolve, reject) {
            var outputStream = ParserStream.createOutputStream(_this.outputPath.replace(".json", ".fields.json"), resolve, reject);
            _this.pdfParser
                .getAllFieldsTypesStream()
                .pipe(new StringifyStream())
                .pipe(outputStream);
        });
    };
    PDFProcessor.prototype.processAdditionalStreams = function () {
        var outputTasks = [];
        if (PROCESS_FIELDS_CONTENT) {
            //needs to generate fields.json file
            outputTasks.push(this.generateFieldsTypesStream());
        }
        if (PROCESS_RAW_TEXT_CONTENT) {
            //needs to generate content.txt file
            outputTasks.push(this.generateRawTextContentStream());
        }
        if (PROCESS_MERGE_BROKEN_TEXT_BLOCKS) {
            //needs to generate json file with merged broken text blocks
            outputTasks.push(this.generateMergedTextBlocksStream());
        }
        return Promise.allSettled(outputTasks);
    };
    PDFProcessor.prototype.onPrimarySuccess = function (resolve, reject) {
        this.curCLI.addResultCount();
        this.processAdditionalStreams()
            .then(function (retVal) { return resolve(retVal); })
            .catch(function (err) { return reject(err); });
    };
    PDFProcessor.prototype.onPrimaryError = function (err, reject) {
        this.curCLI.addResultCount(err);
        reject(err);
    };
    PDFProcessor.prototype.parseOnePDFStream = function () {
        var _this = this;
        return new Promise(function (resolve, reject) {
            _this.pdfParser = new pdfparser_js_1.default(null, PROCESS_RAW_TEXT_CONTENT);
            _this.pdfParser.on("pdfParser_dataError", function (evtData) {
                return _this.onPrimaryError(evtData.parserError, reject);
            });
            var outputStream = fs.createWriteStream(_this.outputPath);
            outputStream.on("finish", function () { return _this.onPrimarySuccess(resolve, reject); });
            outputStream.on("error", function (err) { return _this.onPrimaryError(err, reject); });
            console.info("Transcoding Stream ".concat(_this.inputFile, " to - ").concat(_this.outputPath));
            var inputStream = fs.createReadStream(_this.inputPath);
            inputStream
                .pipe(_this.pdfParser.createParserStream())
                .pipe(new StringifyStream())
                .pipe(outputStream);
        });
    };
    PDFProcessor.prototype.parseOnePDF = function () {
        var _this = this;
        return new Promise(function (resolve, reject) {
            _this.pdfParser = new pdfparser_js_1.default(null, PROCESS_RAW_TEXT_CONTENT);
            _this.pdfParser.on("pdfParser_dataError", function (evtData) {
                return _this.onPrimaryError(evtData.parserError, reject);
            });
            _this.pdfParser.on("pdfParser_dataReady", function (evtData) {
                fs.writeFile(_this.outputPath, JSON.stringify(evtData), function (err) {
                    if (err) {
                        _this.onPrimaryError(err, reject);
                    }
                    else {
                        _this.onPrimarySuccess(resolve, reject);
                    }
                });
            });
            console.info("Transcoding File ".concat(_this.inputFile, " to - ").concat(_this.outputPath));
            _this.pdfParser.loadPDF(_this.inputPath, VERBOSITY_LEVEL);
        });
    };
    //public methods
    PDFProcessor.prototype.validateParams = function () {
        var retVal = '';
        if (!fs.existsSync(this.inputDir))
            retVal =
                "Input error: input directory doesn't exist - ".concat(this.inputDir, ".");
        else if (!fs.existsSync(this.inputPath))
            retVal =
                "Input error: input file doesn't exist - ".concat(this.inputPath, ".");
        else if (!fs.existsSync(this.outputDir))
            retVal =
                "Input error: output directory doesn't exist - ".concat(this.outputDir, ".");
        if (retVal !== null) {
            this.curCLI.addResultCount(retVal);
            return retVal;
        }
        var inExtName = path_1.default.extname(this.inputFile).toLowerCase();
        if (inExtName !== ".pdf") {
            retVal =
                "Input error: input file name doesn't have pdf extention  - ".concat(this.inputFile, ".");
        }
        else {
            this.outputFile = "".concat(path_1.default.basename(this.inputPath, inExtName), ".json");
            this.outputPath = path_1.default.normalize("".concat(this.outputDir, "/").concat(this.outputFile));
            if (fs.existsSync(this.outputPath)) {
                console.warn("Output file will be replaced - ".concat(this.outputPath));
            }
            else {
                var fod = fs.openSync(this.outputPath, "wx");
                if (!fod)
                    retVal = "Input error: can not write to ".concat(this.outputPath);
                else {
                    fs.closeSync(fod);
                    fs.unlinkSync(this.outputPath);
                }
            }
        }
        return retVal;
    };
    PDFProcessor.prototype.destroy = function () {
        this.inputDir = '';
        this.inputFile = '';
        this.inputPath = '';
        this.outputDir = '';
        this.outputPath = '';
        if (this.pdfParser) {
            this.pdfParser.destroy();
        }
        this.pdfParser = null;
        this.curCLI = null;
    };
    PDFProcessor.prototype.processFile = function () {
        var _this = this;
        return new Promise(function (resolve, reject) {
            var validateMsg = _this.validateParams();
            if (validateMsg) {
                reject(validateMsg);
            }
            else {
                var parserFunc = PROCESS_WITH_STREAM
                    ? _this.parseOnePDFStream
                    : _this.parseOnePDF;
                parserFunc
                    .call(_this)
                    .then(function (value) { return resolve(value); })
                    .catch(function (err) { return reject(err); });
            }
        });
    };
    return PDFProcessor;
}());
var PDFCLI = /** @class */ (function () {
    // constructor
    function PDFCLI() {
        this.inputCount = 0;
        this.successCount = 0;
        this.failedCount = 0;
        this.warningCount = 0;
        this.statusMsgs = [];
        this.inputCount = 0;
        this.successCount = 0;
        this.failedCount = 0;
        this.warningCount = 0;
        this.statusMsgs = [];
    }
    PDFCLI.prototype.initialize = function () {
        // eslint-disable-next-line @typescript-eslint/ban-ts-comment
        // @ts-ignore
        nodeUtil.verbosity(VERBOSITY_LEVEL);
        var retVal = true;
        try {
            if (ONLY_SHOW_VERSION) {
                console.log(pkInfo.version);
                retVal = false;
            }
            else if (ONLY_SHOW_HELP) {
                p2jcliarg_js_1.yargs.showHelp();
                retVal = false;
            }
            else if (!HAS_INPUT_DIR_OR_FILE) {
                p2jcliarg_js_1.yargs.showHelp();
                console.error("-f is required to specify input directory or file.");
                retVal = false;
            }
        }
        catch (e) {
            console.error("Exception: ".concat(e.message));
            retVal = false;
        }
        return retVal;
    };
    PDFCLI.prototype.start = function () {
        return __awaiter(this, void 0, void 0, function () {
            var inputStatus, e_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        if (!this.initialize() || !INPUT_DIR_OR_FILE) {
                            console.error("Invalid input parameters.");
                            return [2 /*return*/];
                        }
                        console.log(_PRO_TIMER);
                        console.time(_PRO_TIMER);
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 6, 7, 8]);
                        inputStatus = fs.statSync(INPUT_DIR_OR_FILE);
                        if (!inputStatus.isFile()) return [3 /*break*/, 3];
                        this.inputCount = 1;
                        return [4 /*yield*/, this.processOneFile(path_1.default.dirname(INPUT_DIR_OR_FILE), path_1.default.basename(INPUT_DIR_OR_FILE))];
                    case 2:
                        _a.sent();
                        return [3 /*break*/, 5];
                    case 3:
                        if (!inputStatus.isDirectory()) return [3 /*break*/, 5];
                        return [4 /*yield*/, this.processOneDirectory(path_1.default.normalize(INPUT_DIR_OR_FILE))];
                    case 4:
                        _a.sent();
                        _a.label = 5;
                    case 5: return [3 /*break*/, 8];
                    case 6:
                        e_1 = _a.sent();
                        console.error("Exception: ", e_1);
                        return [3 /*break*/, 8];
                    case 7:
                        this.complete();
                        return [7 /*endfinally*/];
                    case 8: return [2 /*return*/];
                }
            });
        });
    };
    PDFCLI.prototype.complete = function () {
        if (this.statusMsgs.length > 0)
            console.log(this.statusMsgs);
        console.log("".concat(this.inputCount, " input files\t").concat(this.successCount, " success\t").concat(this.failedCount, " fail\t").concat(this.warningCount, " warning"));
        process.nextTick(function () {
            console.timeEnd(_PRO_TIMER);
            // process.exit((this.inputCount === this.successCount) ? 0 : 1);
        });
    };
    PDFCLI.prototype.processOneFile = function (inputDir, inputFile) {
        var _this = this;
        return new Promise(function (resolve, reject) {
            var p2j = new PDFProcessor(inputDir, inputFile, _this);
            p2j
                .processFile()
                // eslint-disable-next-line @typescript-eslint/no-explicit-any
                .then(function (retVal) {
                _this.addStatusMsg(null, "".concat(path_1.default.join(inputDir, inputFile), " => ").concat(p2j.getOutputFile()));
                retVal.forEach(function (ret) { return _this.addStatusMsg(null, "+ ".concat(ret.value)); });
                resolve(retVal);
            })
                .catch(function (error) {
                _this.addStatusMsg(error, "".concat(path_1.default.join(inputDir, inputFile), " => ").concat(error));
                reject(error);
            })
                .finally(function () { return p2j.destroy(); });
        });
    };
    PDFCLI.prototype.processFiles = function (inputDir, files) {
        var _this = this;
        var allPromises = [];
        files.forEach(function (file, idx) {
            return allPromises.push(_this.processOneFile(inputDir, file));
        });
        return Promise.allSettled(allPromises);
    };
    PDFCLI.prototype.processOneDirectory = function (inputDir) {
        var _this = this;
        return new Promise(function (resolve, reject) {
            fs.readdir(inputDir, function (err, files) {
                if (err) {
                    _this.addStatusMsg(true, "[".concat(inputDir, "] - ").concat(err.toString()));
                    reject(err);
                }
                else {
                    var _iChars_1 = "!@#$%^&*()+=[]\\';,/{}|\":<>?~`.-_  ";
                    var pdfFiles = files.filter(function (file) {
                        return file.slice(-4).toLowerCase() === ".pdf" &&
                            _iChars_1.indexOf(file.substring(0, 1)) < 0;
                    });
                    _this.inputCount = pdfFiles.length;
                    if (_this.inputCount > 0) {
                        _this.processFiles(inputDir, pdfFiles)
                            .then(function (value) { return resolve(value); })
                            .catch(function (err) { return reject(err); });
                    }
                    else {
                        _this.addStatusMsg(true, "[".concat(inputDir, "] - No PDF files found"));
                        resolve('no pdf files found');
                    }
                }
            });
        });
    };
    PDFCLI.prototype.addStatusMsg = function (error, oneMsg) {
        this.statusMsgs.push(error ? "\u2717 Error : ".concat(oneMsg) : "\u2713 Success : ".concat(oneMsg));
    };
    PDFCLI.prototype.addResultCount = function (error) {
        error ? this.failedCount++ : this.successCount++;
    };
    return PDFCLI;
}());
exports.default = PDFCLI;

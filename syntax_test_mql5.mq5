// SYNTAX TEST "Packages/Mql5LanguagePack/Mql5LanguagePack.sublime-syntax"

// Comments: https://www.mql5.com/en/docs/basis/syntax/commentaries
/**
 * This is a test file for the Mql5 Syntax Highlighting.
 *
 * Press 'crtl+b' to run the syntax tests.
 */
// <- comment.block.c

// Syntax highlighting for comments is reused from C syntax
// ^ comment.line.double-slash.c

// Includes: https://www.mql5.com/en/docs/basis/preprosessor/include
// With double quoted string
#include "mylib.mqh"
// <- keyword.control.import.include.mql5
// <- meta.preprocessor.include.mql5
//       ^ punctuation.definition.string.begin.mql5
//                 ^ punctuation.definition.string.end.mql5
//          ^ string.quoted.double.include.mql5
//          ^ meta.preprocessor.include.mql5

// With angle brackets
#include <WinUser32.mqh>
// <- keyword.control.import.include.mql5
// <- meta.preprocessor.include.mql5
//       ^ punctuation.definition.string.begin.mql5
//                     ^ punctuation.definition.string.end.mql5
//          ^ string.quoted.other.lt-gt.include.mql5
//          ^ meta.preprocessor.include.mql5

// Imports: https://www.mql5.com/en/docs/basis/preprosessor/import
#import "stdlib.ex5"
// <- keyword.control.import.include.mql5
// <- meta.preprocessor.include.mql5
//      ^ punctuation.definition.string.begin.mql5
//                 ^ punctuation.definition.string.end.mql5
//          ^ meta.preprocessor.include.mql5
string ErrorDescription(int error_code);
#import
// <- keyword.control.import.include.mql5
//   ^ meta.preprocessor.include.mql5

// Define: https://www.mql5.com/en/docs/basis/preprosessor/constant
#define A 2+3
// <- keyword.control.define.mql5
//      ^ entity.name.constant.preprocessor.mql5
//        ^ meta.preprocessor.macro.mql5

#define MUL(a, b) ((a)* /* comment block */ (b))
//      ^^^ entity.name.function.preprocessor.mql5
//          ^ meta.preprocessor.macro.parameters.mql5
//             ^ meta.preprocessor.macro.parameters.mql5
//                                            ^ meta.preprocessor.macro.mql5

// Multi line define directive ends with last line
#define assertFalseOrExit(cond, msg) \
  if ((cond)) { \
    Alert(msg + " - Assert fail on " + #cond + " in " + __FILE__ + ":" + (string) __LINE__); \
    ExpertRemove(); \
  }
// <- meta.preprocessor.macro.mql5

// Conditional compilation: https://www.mql5.com/en/docs/basis/preprosessor/conditional_compilation
#ifdef _DEBUG
// <- keyword.control.import.mql5
    Print("Hello from MQL5 compiler [DEBUG]");
#else
// <- keyword.control.import.mql5
    #ifdef _RELEASE
//  ^ keyword.control.import.mql5
        Print("Hello from MQL5 compiler [RELEASE]");
    #endif
//  ^ keyword.control.import.mql5
#endif
// <- keyword.control.import.mql5
#undef _RELEASE
// <- keyword.control.import.mql5

// To be sure assert that we do not hightlight not supported C macros
#pragma
// <- - keyword.control.import.mql5
#if
// <- - keyword.control.import.mql5

// Inputs: https://www.mql5.com/en/docs/basis/variables/inputvariables
// For now we take inputs as a base type
input group           "Signal"
// <- storage.type.mql5
//    ^ storage.type.mql5
input int             ExtBBPeriod   = 20;       // Bollinger Bands period
input double          ExtBBDeviation= 2.0;      // deviation
input ENUM_TIMEFRAMES ExtSignalTF=PERIOD_M15;   // BB timeframe

// Integer Types: https://www.mql5.com/en/docs/basis/types/integer
char a = -128;
// <- storage.type.mql5
uchar b = 12;
// <- storage.type.mql5
bool c = true;
// <- storage.type.mql5
short d = -1;
// <- storage.type.mql5
ushort e = 1;
// <- storage.type.mql5
int f = -1234567890;
// <- storage.type.mql5
uint g = 1234567890;
// <- storage.type.mql5
color h = 16777215;
// <- storage.type.mql5
long i = -16777215;
// <- storage.type.mql5
ulong j = 16777215;
// <- storage.type.mql5
datetime k = 16777215;
// <- storage.type.mql5

// Real Types: https://www.mql5.com/en/docs/basis/types/double
double l = 12.111;
// <- storage.type.mql5
float m = 0.0001;
// <- storage.type.mql5

// String Type: https://www.mql5.com/en/docs/basis/types/stringconst
string svar="This is a character string";
// <- storage.type.mql5

// Complex Types: https://www.mql5.com/en/docs/basis/types/classes
struct trade_settings {
// <- storage.type.mql5
   uchar  slippage;     // value of the permissible slippage-size 1 byte
   char   reserved1;    // skip 1 byte
   short  reserved2;    // skip 2 bytes
   int    reserved4;    // another 4 bytes are skipped. ensure alignment of the boundary 8 bytes
   double take;         // values of the price of profit fixing
   double stop;         // price value of the protective stop
};

// To be sure assert that we do not highlight C types that are not available in Mql5
signed d = 1;
// <- - storage.type.c
// <- - storage.type.c++

// Visibillity Modifiers
class TradeSettings : public Settings {
// <- storage.type.mql5
//                      ^ storage.modifier.mql5
private:
// ^ storage.modifier.mql5
    static uchar  slippage;     // value of the permissible slippage-size 1 byte
//  ^ storage.modifier.mql5
//         ^ storage.type.mql5
    char   reserved1;    // skip 1 byte
protected:
// ^ storage.modifier.mql5
    short  reserved2;    // skip 2 bytes
    int    reserved4;    // another 4 bytes are skipped. ensure alignment of the boundary 8 bytes
    double take;         // values of the price of profit fixing
    double stop;         // price value of the protective stop
public:
// ^ storage.modifier.mql5
    TradeSettings();
    ~TradeSettings();
};

// Long string with escapings
string HTML_head="<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\""
//               ^ punctuation.definition.string.begin.mql5
//                                                                                ^ punctuation.definition.string.end.mql5
                    " \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n"
//                    ^ constant.character.escape.mql5
                    "<html xmlns=\"http://www.w3.org/1999/xhtml\">\n"
                    "<head>\n"
//                          ^ constant.character.escape.mql5
                    "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />\n"
                    "<title>Trade Operations Report</title>\n"
                    "</head>";
                    // <- string.quoted.double.mql5

// Functions:
int somefunc(double a, double d=0.0001,
             int n=5, bool b=true,
             string s="passed string")
  {
   Print("Required parameter a = ",a);
   Print("Pass the following parameters: d = ",d," n = ",n," b = ",b," s = ",s);
   return(0);
  }

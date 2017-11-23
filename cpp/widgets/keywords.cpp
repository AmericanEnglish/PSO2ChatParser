#include <keywords.h>
#include <QGridLayout>
#include <QPlainTextEdit>
#include <QLabel>
#include <QRadioButton>
#include <QButtonGroup>
#include <QHBoxLayout>
#include <QWidget>

Keywords::Keywords(QWidget *parent) : QWidget(parent) {
    setWindowTitle("Keywords and Phrase");
    // Grid
    QGridLayout *grid = new QGridLayout();
    
    // Text box
    QLabel *textlabel = new QLabel("Type in words. Words seperated by spaces and \",\"", this);
    text = new QPlainTextEdit(this);

    // Radio Buttons
    radioGroup = new QButtonGroup(this);
    QLabel *radioLabel = new QLabel("Search using ...", this);
    phrase = new QRadioButton("Phrase", this);
    words = new QRadioButton("Words", this);
    nothing = new QRadioButton("Nothing", this);

    radioGroup->addButton(phrase, 0);
    radioGroup->addButton(words, 1);
    radioGroup->addButton(nothing, 2);

    QWidget *radios = new QWidget();
    QHBoxLayout *radiolayout = new QHBoxLayout();
    radiolayout->addWidget(phrase);
    radiolayout->addWidget(words);
    radiolayout->addWidget(nothing);
    radios->setLayout(radiolayout);


    nothing->setChecked(true);

    casing = new QCheckBox("Case Senstive?");
    relative = new QCheckBox("Absolute Match Terms?");



    // Layout
    grid->addWidget(textlabel, 0, 0);
    grid->addWidget(text, 1, 0, 3, 4);
    grid->addWidget(radioLabel, 4, 0);
    grid->addWidget(casing, 4, 2);
    grid->addWidget(relative, 5, 2);
    grid->addWidget(radios, 5, 0, 5, 2);

    setLayout(grid);
    
    

}

QRegularExpression Keywords::rLiquidate() {
    QStringList results;
    QRegularExpression re;
    if (nothing->isChecked()) {
        re.setPattern("[\\s\\S]*");
        re.setPatternOptions(
            QRegularExpression::UseUnicodePropertiesOption |
            QRegularExpression::OptimizeOnFirstUsageOption);
        return re;
    }
    else {
        QString all_words = text->toPlainText();
        if (words->isChecked()) {
            QStringList results = all_words.split(QRegExp("\\s+|,"));
        }
        else {
            QStringList results;
            results.append(all_words);
        }
        if (relative->isChecked()) {
            // results << "not relative";
            // Adjust words to be matches absolutely
            QStringList adjusted;
            for (int i = 0; i < results.length(); i++) {
                adjusted.append("(\\W|^)" + results.at(i) + "(\\W|$)");
            }
            re.setPattern(adjusted.join("|"));
            if (casing->isChecked()) {
                // results << "sensitive";
                re.setPatternOptions(
                    QRegularExpression::UseUnicodePropertiesOption |
                    QRegularExpression::OptimizeOnFirstUsageOption);
            }
            else {
                re.setPatternOptions(QRegularExpression::CaseInsensitiveOption |
                    QRegularExpression::UseUnicodePropertiesOption |
                    QRegularExpression::OptimizeOnFirstUsageOption);
                // << "not sensitive";
            }
        }
        else {
            // results << "relative";
            re.setPattern(results.join("|"));
            if (casing->isChecked()) {
                re.setPatternOptions(
                    QRegularExpression::UseUnicodePropertiesOption |
                    QRegularExpression::OptimizeOnFirstUsageOption);
                results << "sensitive";
            }
            else {
                re.setPatternOptions(QRegularExpression::CaseInsensitiveOption |
                    QRegularExpression::UseUnicodePropertiesOption |
                    QRegularExpression::OptimizeOnFirstUsageOption);
                results << "not sensitive";
            }
        }
    }
    // qDebug() << re;
    return re;


}

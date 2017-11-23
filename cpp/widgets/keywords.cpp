#include <keywords.h>
#include <QGridLayout>
#include <QPlainTextEdit>
#include <QLabel>
#include <QRadioButton>
#include <QButtonGroup>
#include <QHBoxLayout>
#include <QWidget>
#include <QDebug>

Keywords::Keywords(QWidget *parent) : QWidget(parent) {
    setWindowTitle("Keywords and Phrase");
    // Grid
    QGridLayout *grid = new QGridLayout();
    
    // Text box
    QLabel *textlabel = new QLabel("Type in words. Words seperated by spaces and \",\"", this);
    text = new QPlainTextEdit(this);

    // Radio Buttons
    radioGroup = new QButtonGroup(this);
    QButtonGroup *boolCheckGroup = new QButtonGroup(this);
    QLabel *radioLabel = new QLabel("Search using ...", this);
    phrase = new QRadioButton("Phrase", this);
    words = new QRadioButton("Words", this);
    nothing = new QRadioButton("Nothing", this);
    orCheckBox = new QCheckBox("Or", this);
    QCheckBox *andCheckBox = new QCheckBox("And", this);

    radioGroup->addButton(phrase, 0);
    radioGroup->addButton(words, 1);
    radioGroup->addButton(nothing, 2);
    boolCheckGroup->addButton(orCheckBox, 0);
    boolCheckGroup->addButton(andCheckBox, 1);

    QWidget *radios = new QWidget(this);
    QHBoxLayout *radiolayout = new QHBoxLayout(this);
    radiolayout->addWidget(phrase);
    radiolayout->addWidget(words);
    radiolayout->addWidget(nothing);
    radiolayout->setAlignment(Qt::AlignCenter);
    radios->setLayout(radiolayout);
    
    nothing->setChecked(true);
    orCheckBox->setChecked(true);

    casing = new QCheckBox("Case Senstive?");
    absolute = new QCheckBox("Absolute Match Terms?");



    // Layout
    grid->addWidget(textlabel, 0, 0);
    grid->addWidget(text, 1, 0, 3, 4);
    grid->addWidget(radioLabel, 4, 0);
    grid->addWidget(casing, 5, 2, 1, 2);
    grid->addWidget(absolute, 6, 2, 1, 2);
    grid->addWidget(radios, 5, 0, 3, 1);
    // grid->addWidget(boolRadios,7, 0, 1, 1);
    // grid->addWidget(boolBoxes,7, 2);
    grid->addWidget(orCheckBox, 7, 2);
    grid->addWidget(andCheckBox, 7, 3);

    setLayout(grid);
    
    

}

QRegularExpression Keywords::rLiquidate() {
    QStringList results;
    QRegularExpression re;
    QString output;
    if (nothing->isChecked()) {
        output = "[\\s\\S]*";
        qDebug() << "\\Keyword Regex:" << output;
        re.setPattern(output);
        re.setPatternOptions(
            QRegularExpression::UseUnicodePropertiesOption |
            QRegularExpression::OptimizeOnFirstUsageOption);
        return re;
    }

    else {
        QString all_words = text->toPlainText();
        if (words->isChecked()) {
            results = all_words.split(QRegExp("\\s+|,"));
            qDebug() << all_words << ":Split To->:" << results;
        }
        else {
            results.append(all_words);
        }

        if (absolute->isChecked()) {
            if (orCheckBox->isChecked()) { // Absolute OR
                output = createRegex(results, true, false);
            }
            else { // Absolute AND
                output = createRegex(results, false, false);
            }
            qDebug() << "\\Keyword Regex:" << output;
            re.setPattern(output);
            if (casing->isChecked()) {
                re.setPatternOptions(
                    QRegularExpression::UseUnicodePropertiesOption |
                    QRegularExpression::OptimizeOnFirstUsageOption);
            }
            else {
                re.setPatternOptions(QRegularExpression::CaseInsensitiveOption |
                    QRegularExpression::UseUnicodePropertiesOption |
                    QRegularExpression::OptimizeOnFirstUsageOption);
            }
        }
        else { 
            if (orCheckBox->isChecked()) { // Relative OR
                output = createRegex(results, true, true);
            }
            else { // Relative AND
                output = createRegex(results, false, true);
            }
            qDebug() << "\\Keyword Regex:" << output;
            re.setPattern(output);
            if (casing->isChecked()) {
                re.setPatternOptions(
                    QRegularExpression::UseUnicodePropertiesOption |
                    QRegularExpression::OptimizeOnFirstUsageOption);
            }
            else {
                re.setPatternOptions(QRegularExpression::CaseInsensitiveOption |
                    QRegularExpression::UseUnicodePropertiesOption |
                    QRegularExpression::OptimizeOnFirstUsageOption);
            }
        }
    }
    // qDebug() << re;
    return re;
}

QString Keywords::createRegex(QStringList words, bool OR, bool relative) { // Absolute ORs and ANDs
    QStringList results;
    for (int i = 0; i < words.length(); i++) {
        if (OR && !relative) { // Absolute OR matching
            results.append("\\b" + words.at(i) + "\\b");
        }
        else if (!OR && !relative) { // Absolute AND matching
            results.append("(?=.*\\b"+words.at(i)+"\\b)");
        }
        else if (!OR && relative) { // Relative AND matching
            results.append("(?=.*" + words.at(i) + ")");
        }
        else { // Relative OR matching
            results.append(words.at(i));
        }
    }
    if (OR) {
        return results.join("|");
    }
    else {
        return results.join("") + ".*";
    }
} 

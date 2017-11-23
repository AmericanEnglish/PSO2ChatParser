#include <chattype.h>
#include <QCheckBox>
#include <QGridLayout>
#include <QStringList>
#include <QWidget>
#include <QRegularExpression>


ChatType::ChatType(QWidget *parent) : QWidget(parent) {
    setWindowTitle("Chat Type Selection");
    // Grid
    QGridLayout *grid = new QGridLayout();
    
    // Boxes
    publix = new QCheckBox("Public", this);
    publix->setChecked(true);
    party = new QCheckBox("Party", this);
    party->setChecked(true);
    guild = new QCheckBox("Team", this);
    guild->setChecked(true);
    reply = new QCheckBox("Whisper", this);
    reply->setChecked(true);

    // Add to grid
    grid->addWidget(publix, 0, 0);
    grid->addWidget(party, 0, 1);
    grid->addWidget(guild, 0, 2);
    grid->addWidget(reply, 0, 3);
    setLayout(grid);

}

QRegularExpression ChatType::rLiquidate() {
    QStringList results;
    if (publix->isChecked()) {
        results.append("PUBLIC");
    }
    if (party->isChecked()) {
        results.append("PARTY");
    }
    if (guild->isChecked()) {
        results.append("GUILD");
    }
    if (reply->isChecked()) {
        results.append("REPLY");
    }
    QRegularExpression re(results.join("|"));
    re.setPatternOptions(
        QRegularExpression::UseUnicodePropertiesOption |
        QRegularExpression::OptimizeOnFirstUsageOption);
    return re;
}

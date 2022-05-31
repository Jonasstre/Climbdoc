#ifndef INITIALS_H
#define INITIALS_H

#include <QWidget>

namespace Ui {
class initials;
}

class initials : public QWidget
{
    Q_OBJECT

public:
    explicit initials(QWidget *parent = nullptr);
    ~initials();

private:
    Ui::initials *ui;
};

#endif // INITIALS_H

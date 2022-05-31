#ifndef ARDNOTFOUND_H
#define ARDNOTFOUND_H

#include <QWidget>

namespace Ui {
class ardnotfound;
}

class ardnotfound : public QWidget
{
    Q_OBJECT

public:
    explicit ardnotfound(QWidget *parent = nullptr);
    ~ardnotfound();

private:
    Ui::ardnotfound *ui;
};

#endif // ARDNOTFOUND_H

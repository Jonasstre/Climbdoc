#include "ardnotfound.h"
#include "ui_ardnotfound.h"

ardnotfound::ardnotfound(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::ardnotfound)
{
    ui->setupUi(this);
}

ardnotfound::~ardnotfound()
{
    delete ui;
}

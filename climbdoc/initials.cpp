#include "initials.h"
#include "ui_initials.h"

initials::initials(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::initials)
{
    ui->setupUi(this);
}

initials::~initials()
{
    delete ui;
}

#include <stdio.h>
#include <math.h>
#include "Python.h"

#define CONST_GRAVITACIONAL 6.67428 * pow(10.0, -11.0)
#define C 299.792458

void initcontas(void);

main(int argc, char **argv){
	// Inicializa o Interpretador python embutido
	Py_Initialize();
	// Adiciona o nosso modulo
	initcontas();
	// Sai do interpretador embutido.
	Py_Exit(0);
}

static PyObject *contas_forc(PyObject *self, PyObject* args){
	double x_diff, y_diff, distance, force, dist;
	double ax, ay, ar, am, bx, by, br, bm;

	if (!PyArg_ParseTuple(args, "dddddddd", &ax , &ay , &ar , &am , &bx , &by , &br, &bm)) {
		return NULL;
	}
	x_diff = ax - bx;
	y_diff = ay - by;

	dist = sqrt(x_diff*x_diff + y_diff*y_diff);
	if(dist < (ar + br)) {
		dist = ar + br;
	}

	/* Changing the units. Using pure numbers instead of pow().
	 * It should increase the performance!
	 */
	am = am * 10000000000;
	bm = bm * 10000000000;
	dist = dist * 1000000;

	force = (CONST_GRAVITACIONAL * am * bm) / (dist*dist); //F = (Constant*massA*massB)/dist**2

	return PyFloat_FromDouble(force);
}

static PyObject *contas_dist(PyObject *self, PyObject* args){
	double x_diff, y_diff, distance, force, dist;
	double ax, ay, ar, am, bx, by, br, bm;

	if (!PyArg_ParseTuple(args, "dddddd", &ax , &ay, &ar , &bx , &by, &br)) {
		return NULL;
	}
	x_diff = ax - bx;
	y_diff = ay - by;

	dist = sqrt(x_diff*x_diff + y_diff*y_diff);
	if(dist < (ar + br)) {
		dist = ar + br;
	}

	return PyFloat_FromDouble(dist);
}


static PyObject *contas_relativistic_mass(PyObject *self, PyObject* args){

	double a_speedx , a_speedy, a_mass, relativistic_mass, abs_speed;

	if (!PyArg_ParseTuple(args, "ddd", &a_speedx , &a_speedy, &a_mass)){
		return NULL;
	}

	abs_speed = sqrt(a_speedx + a_speedy);
	relativistic_mass = a_mass / sqrt( 1- (abs_speed * abs_speed) / (C * C) );

	return PyFloat_FromDouble(relativistic_mass);
}


static PyMethodDef contas_methods[] = {
	{"forc",contas_forc,METH_VARARGS, "Return the Force of interaction between 2 bodies - (a_x,a_y,a_radio,a_mass,b_x,b_y,b_radio,b_mass)"},
	{"dist",contas_dist,METH_VARARGS, "Return the distance between 2 bodies - (a_x,a_y,a_radio,b_x,b_y,b_radio)"},
	{"relativistic_mass",contas_relativistic_mass,METH_VARARGS, "Return the relativistic mass of a body."},
	{NULL, NULL} //sentinela
};

void initcontas(void) {
	PyImport_AddModule("contas");
	Py_InitModule("contas", contas_methods);
}

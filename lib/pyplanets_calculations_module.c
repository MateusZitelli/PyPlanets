#include <stdio.h>
#include <math.h>
#include "Python.h"

#define CONST_GRAVITACIONAL 6.67428 * pow(10.0, -11.0)
#define C 299.792458

void initpyplanets_calculations(void);

main(int argc, char **argv){
	// Inicializa o Interpretador python embutido
	Py_Initialize();
	// Adiciona o nosso modulo
	initpyplanets_calculations();
	// Sai do interpretador embutido.
	Py_Exit(0);
}

static PyObject *pyplanets_calculations_forc(PyObject *self, PyObject* args){
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

static PyObject *pyplanets_calculations_dist(PyObject *self, PyObject* args){
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


static PyObject *pyplanets_calculations_relativistic_mass(PyObject *self, PyObject* args){

	double a_speedx , a_speedy, a_mass, relativistic_mass, abs_speed;

	if (!PyArg_ParseTuple(args, "ddd", &a_speedx , &a_speedy, &a_mass)){
		return NULL;
	}

	abs_speed = sqrt(a_speedx*a_speedx + a_speedy*a_speedy);
	relativistic_mass = a_mass / sqrt( 1- (abs_speed * abs_speed) / (C * C) );

	return PyFloat_FromDouble(relativistic_mass);
}


static PyObject *pyplanets_calculations_collision(PyObject *self, PyObject* args){
	double a_x , a_y , a_speedx , a_speedy, a_mass , a_raio , b_x , b_y , b_speedx , b_speedy, b_mass, b_raio , collision_x , collision_y, theta , rx , ry , tamanho;
	double trans_ax , trans_ay , trans_bx , trans_by, cinecte, restituition , array[8];
	int i;

	if (!PyArg_ParseTuple(args, "dddddddddddd", &a_x , &a_y , &a_speedx , &a_speedy, &a_mass, &a_raio , &b_x , &b_y , &b_speedx , &b_speedy, &b_mass , &b_raio)){
		return NULL;
	}

	restituition = 0.5;

	collision_x = (a_x - b_x);
	collision_y = (a_y - b_y);
	tamanho = sqrt( collision_x*collision_x + collision_y*collision_y );

	theta = 1/cos( ( a_speedx * collision_x )/( sqrt( a_speedx*a_speedx ) * sqrt( collision_x*collision_x ) ) );
	trans_ax = a_speedx*cos(theta);
	theta = 1/cos( ( a_speedy * collision_y )/( sqrt( a_speedy*a_speedy ) * sqrt( collision_y*collision_y ) ) );
	trans_ay = a_speedy*cos(theta);
	
	theta = 1/cos( ( b_speedx * collision_x )/( sqrt( b_speedx*b_speedx ) * sqrt( collision_x*collision_x ) ) );
	trans_bx = b_speedx*cos(theta);
	theta = 1/cos( ( b_speedy * collision_y )/( sqrt( b_speedy*b_speedy ) * sqrt( collision_y*collision_y ) ) );
	trans_by = b_speedy*cos(theta);

	rx = (collision_x/tamanho * (a_raio+b_raio)) - collision_x;
	ry = (collision_y/tamanho * (a_raio+b_raio)) - collision_y;

	a_x += rx/2.0;
	a_y += ry/2.0;
	b_x -= rx/2.0;
	b_y -= ry/2.0;

	cinecte = a_mass/(a_mass+b_mass);
	a_speedx *= cinecte;
	a_speedy *= cinecte;
	cinecte = b_mass/(a_mass+b_mass);
	b_speedx *= cinecte;
	b_speedy *= cinecte;

	a_speedx += (trans_bx-trans_ax)*restituition;
	a_speedy += (trans_by-trans_ay)*restituition;
	b_speedx *= (trans_ax-trans_bx)*restituition;
	b_speedy *= (trans_ay-trans_by)*restituition;
	
	array[0] = a_x;
	array[1] = a_y;
	array[2] = b_x;
	array[3] = b_y;
	array[4] = a_speedx;
	array[5] = a_speedy;
	array[6] = b_speedx;
	array[7] = b_speedy;

	PyObject *lst = PyList_New(8);
	if (!lst) return NULL;
	for (i = 0; i < 8; i++) {
		PyObject *num = PyFloat_FromDouble(array[i]);
		if (!num) {
			Py_DECREF(lst);
			return NULL;
		}
	PyList_SET_ITEM(lst, i, num);
	}
	return lst;
}

static PyMethodDef pyplanets_calculations_methods[] = {
	{"forc",pyplanets_calculations_forc,METH_VARARGS, "Return the Force of interaction between 2 bodies - (a_x,a_y,a_radio,a_mass,b_x,b_y,b_radio,b_mass)"},
	{"dist",pyplanets_calculations_dist,METH_VARARGS, "Return the distance between 2 bodies - (a_x,a_y,a_radio,b_x,b_y,b_radio)"},
	{"relativistic_mass",pyplanets_calculations_relativistic_mass,METH_VARARGS, "Return the relativistic mass of a body."},
	{"collision",pyplanets_calculations_collision,METH_VARARGS, "Return the new location and speed after the collision"},
	{NULL, NULL}
};

void initpyplanets_calculations(void) {
	PyImport_AddModule("pyplanets_calculations");
	Py_InitModule("pyplanets_calculations", pyplanets_calculations_methods);
}

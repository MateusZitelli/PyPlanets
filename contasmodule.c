
#include <stdio.h>
#include <math.h>
#include "Python.h"


// Assinatura do nosso modulo
void initcontas(void);

// Função principal que embute o python dentro do C.
main(int argc, char **argv) {
	// Inicializa o Interpretador python embutido
	Py_Initialize();
	// Adiciona o nosso modulo
	initcontas();
	// Sai do interpretador embutido.
	Py_Exit(0);
}

static PyObject *contas_forc(PyObject *self, PyObject* args)
{
	double const_gravitacional = 6.67428*pow(10.0,-11.0);
	double xdif;
	double ydif;
	double dist;
	double force;
	double  ax , ay , ar , am , bx , by , br, bm;

	if (!PyArg_ParseTuple(args, "dddddddd", &ax , &ay , &ar , &am , &bx , &by , &br, &bm)) {
		return NULL;
	}
	xdif = ax-bx;
	ydif = ay-by;
	dist = sqrt(pow(xdif,2)+pow(ydif,2));
	if(dist < (ar+br))
	{
		dist = br+ar;
	}
	force = (const_gravitacional*am*pow(10,10)*bm*pow(10,10))/pow(dist*pow(10,6),2); //F = (Constant*massA*massB)/dist**2
	return PyFloat_FromDouble(force);
}


static PyMethodDef contas_methods[] = {
	{"forc",contas_forc,METH_VARARGS, "Documentação do argumento_numeros"},
	{NULL, NULL} //sentinela
};

void initcontas(void)
{
	PyImport_AddModule("contas");
	Py_InitModule("contas", contas_methods);
}

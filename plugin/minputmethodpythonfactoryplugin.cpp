 /*
 * Copyright (C) 2011 INdT
 * All rights reserved.
 *
 * If you have questions regarding the use of this file, please contact
 * Nokia at directui@nokia.com.
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License version 2.1 as published by the Free Software Foundation
 * and appearing in the file LICENSE.LGPL included in the packaging
 * of this file.
 */

#include <Python.h>
#include "minputmethodpythonfactoryplugin.h"

#include <shiboken.h>
#include <QString>
#include <QFileInfo>
#include <QDebug>

// FIXME: Hardcoded classes from 0.80 plugins API. Maybe we'll need one
// factory for each plugin api.

namespace {
    MInputMethodPlugin *loadPythonFile(const QString &pythonFile)
    {
        PyObject *mainModule;
        PyObject *mainLocals;
        PyObject *fromlist;
        PyObject *module;
        MInputMethodPlugin *pluginObject;

        Py_Initialize();
        Shiboken::init();
        Shiboken::GilState pyGil;

        // Dummy locals
        mainModule = PyImport_AddModule("__main__");
        mainLocals = PyModule_GetDict(mainModule);

        //Append our plugin path to system
        QFileInfo pluginPath(pythonFile);
        PyObject *sys_path = PySys_GetObject(const_cast<char*>("path"));
        PyObject *path = PyString_FromString(qPrintable(pluginPath.path()));
        if (PySequence_Contains(sys_path, path) == 0)
            PyList_Insert(sys_path, 0, path);
        Py_DECREF(path);

        // Actually load the python plugin
        fromlist = PyTuple_New(0);
        module = PyImport_ImportModuleEx(const_cast<char*>(qPrintable(pluginPath.baseName())), mainLocals, mainLocals, fromlist);
        Py_DECREF(fromlist);
        if (!module) {
            PyErr_Print();
            Py_DECREF(mainModule);
            return 0;
        }

        // Now that maliit is already loaded, get the plugin type to check for
        // plugin implementations in the module.
        Shiboken::TypeResolver* sbkType = Shiboken::TypeResolver::get("MInputMethodPlugin*");
        if (!sbkType) {
            qWarning() << "Plugin type not found.";
            Py_DECREF(module);
            Py_DECREF(mainModule);
            return 0;
        }
        PyObject *pluginType = reinterpret_cast<PyObject*>(sbkType->pythonType());

        Py_ssize_t pos=0;
        PyObject *key;
        PyObject *value;
        PyObject *locals = PyModule_GetDict (module);

        // Search for the plugin class
        while(PyDict_Next(locals, &pos, &key, &value)) {
            if (!PyType_Check(value))
                continue;

            if (PyObject_IsSubclass (value, pluginType) && (value != pluginType)) {
                // Instantiate the plugin
                PyObject *args = PyTuple_New(0);
                PyObject *pyPlugin = PyObject_Call(value, args, 0);
                Py_DECREF(args);
                if (!pyPlugin || PyErr_Occurred()) {
                    PyErr_Print();
                    break;
                }
                pluginObject = reinterpret_cast<MInputMethodPlugin*>(Shiboken::Object::cppPointer(reinterpret_cast<SbkObject*>(pyPlugin),
                                                                                                  reinterpret_cast<PyTypeObject*>(pluginType)));
                if (pluginObject)
                    Shiboken::Object::releaseOwnership(reinterpret_cast<SbkObject*>(pyPlugin)); // transfer ownership to C++

                Py_XDECREF(pyPlugin);
                break;
            }
        }

        Q_ASSERT(pluginObject);
        Py_DECREF(mainModule);
        Py_DECREF(module);

        return pluginObject;
    }
} // namespace

MInputMethodPythonFactoryPlugin::MInputMethodPythonFactoryPlugin()
{
}

MInputMethodPythonFactoryPlugin::~MInputMethodPythonFactoryPlugin()
{
}

QString MInputMethodPythonFactoryPlugin::fileExtension() const
{
    return "py";
}

MInputMethodPlugin* MInputMethodPythonFactoryPlugin::create(const QString &fileName) const
{
    return loadPythonFile(fileName);
}

Q_EXPORT_PLUGIN2(pymaliit, MInputMethodPythonFactoryPlugin)

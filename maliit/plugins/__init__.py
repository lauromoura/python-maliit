
_loaded = False

def require(version):

    global _loaded

    if _loaded:
        raise RuntimeError("Module already configured")
    print "Configuring maliit.plugins to provide api version", version

    if '.' in version:
        version = version.replace('.', '')

    name = 'plugins%s' % version

    root = __import__(__name__ + '.' + name)

    public = getattr(root, 'plugins')
    private = getattr(public, name)

    for member in dir(private):
        if member.startswith('__'):
            continue

        attr = getattr(private, member)
        setattr(public, member, attr)

    _loaded = True

    return _loaded



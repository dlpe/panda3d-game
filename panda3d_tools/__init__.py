import os, sys
import panda3d

if sys.platform in ('win32', 'cygwin'):
    path_var = 'PATH'
elif sys.platform == 'darwin':
    path_var = 'DYLD_LIBRARY_PATH'
else:
    path_var = 'LD_LIBRARY_PATH'

dir = os.path.dirname(panda3d.__file__)
del panda3d
if not os.environ.get(path_var):
    os.environ[path_var] = dir
else:
    os.environ[path_var] = dir + os.pathsep + os.environ[path_var]

del os, sys, path_var, dir


def _exec_tool(tool):
    import os, sys
    from subprocess import Popen
    tools_dir = os.path.dirname(__file__)
    handle = Popen(sys.argv, executable=os.path.join(tools_dir, tool))
    try:
        try:
            return handle.wait()
        except KeyboardInterrupt:
            # Give the program a chance to handle the signal gracefully.
            return handle.wait()
    except:
        handle.kill()
        handle.wait()
        raise

# Register all the executables in this directory as global functions.
egg_mkfont = lambda: _exec_tool(u'egg-mkfont')
flt2egg = lambda: _exec_tool(u'flt2egg')
x_trans = lambda: _exec_tool(u'x-trans')
obj2egg = lambda: _exec_tool(u'obj2egg')
bam2egg = lambda: _exec_tool(u'bam2egg')
apply_patch = lambda: _exec_tool(u'apply_patch')
parse_file = lambda: _exec_tool(u'parse_file')
dae2egg = lambda: _exec_tool(u'dae2egg')
check_crc = lambda: _exec_tool(u'check_crc')
egg_trans = lambda: _exec_tool(u'egg-trans')
egg_optchar = lambda: _exec_tool(u'egg-optchar')
image_info = lambda: _exec_tool(u'image-info')
egg_texture_cards = lambda: _exec_tool(u'egg-texture-cards')
egg_make_tube = lambda: _exec_tool(u'egg-make-tube')
egg_palettize = lambda: _exec_tool(u'egg-palettize')
build_patch = lambda: _exec_tool(u'build_patch')
check_md5 = lambda: _exec_tool(u'check_md5')
flt_info = lambda: _exec_tool(u'flt-info')
vrml_trans = lambda: _exec_tool(u'vrml-trans')
egg2x = lambda: _exec_tool(u'egg2x')
egg_retarget_anim = lambda: _exec_tool(u'egg-retarget-anim')
pfm_bba = lambda: _exec_tool(u'pfm-bba')
image_trans = lambda: _exec_tool(u'image-trans')
egg2c = lambda: _exec_tool(u'egg2c')
image_resize = lambda: _exec_tool(u'image-resize')
flt_trans = lambda: _exec_tool(u'flt-trans')
pzip = lambda: _exec_tool(u'pzip')
pview = lambda: _exec_tool(u'pview')
punzip = lambda: _exec_tool(u'punzip')
egg_qtess = lambda: _exec_tool(u'egg-qtess')
show_ddb = lambda: _exec_tool(u'show_ddb')
dxf_points = lambda: _exec_tool(u'dxf-points')
egg2flt = lambda: _exec_tool(u'egg2flt')
egg2bam = lambda: _exec_tool(u'egg2bam')
egg_topstrip = lambda: _exec_tool(u'egg-topstrip')
pencrypt = lambda: _exec_tool(u'pencrypt')
vrml2egg = lambda: _exec_tool(u'vrml2egg')
interrogate = lambda: _exec_tool(u'interrogate')
fltcopy = lambda: _exec_tool(u'fltcopy')
interrogate_module = lambda: _exec_tool(u'interrogate_module')
pdecrypt = lambda: _exec_tool(u'pdecrypt')
make_prc_key = lambda: _exec_tool(u'make-prc-key')
lwo_scan = lambda: _exec_tool(u'lwo-scan')
p3dcparse = lambda: _exec_tool(u'p3dcparse')
softcvs = lambda: _exec_tool(u'softcvs')
egg_rename = lambda: _exec_tool(u'egg-rename')
egg_crop = lambda: _exec_tool(u'egg-crop')
egg2obj = lambda: _exec_tool(u'egg2obj')
egg2dxf = lambda: _exec_tool(u'egg2dxf')
bam_info = lambda: _exec_tool(u'bam-info')
dxf2egg = lambda: _exec_tool(u'dxf2egg')
pfm_trans = lambda: _exec_tool(u'pfm-trans')
x2egg = lambda: _exec_tool(u'x2egg')
check_adler = lambda: _exec_tool(u'check_adler')
multify = lambda: _exec_tool(u'multify')
test_interrogate = lambda: _exec_tool(u'test_interrogate')
egg_list_textures = lambda: _exec_tool(u'egg-list-textures')
text_stats = lambda: _exec_tool(u'text-stats')
lwo2egg = lambda: _exec_tool(u'lwo2egg')


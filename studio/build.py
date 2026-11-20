"""Build the exhibition's original workshop and archival illustrations. Run from repo root with Blender -b -P studio/build.py."""
import bpy, math, os
from mathutils import Vector
from math import pi, sin, cos
from pathlib import Path
ROOT=Path.cwd()
b=bpy; b.ops.wm.read_factory_settings(use_empty=True)
def material(name,rgb,metal=0,rough=.42):
    m=b.data.materials.new(name);m.diffuse_color=(*rgb,1);m.use_nodes=True
    bs=m.node_tree.nodes.get("Principled BSDF");bs.inputs["Base Color"].default_value=(*rgb,1)
    bs.inputs["Metallic"].default_value=metal;bs.inputs["Roughness"].default_value=rough
    return m
steel=material("Turned stainless steel",(.47,.58,.63),.86,.25)
edge=material("Polished bevels",(.72,.79,.81),.92,.21)
dark=material("Gunmetal",(.036,.071,.09),.72,.29)
ink=material("Petrol blue",(.017,.063,.081),.12,.47)
teal=material("Enamel teal",(.027,.30,.30),.32,.27)
brass=material("Machined brass",(.72,.43,.16),.79,.25)
paper=material("Rag paper",(.84,.80,.68),0,.68)
rule=material("Drafting marks",(.59,.77,.72),.03,.49)
char=material("Printed ink",(.07,.11,.13),0,.62)
slate=material("Workshop surface",(.027,.048,.065),.14,.49)
world=b.data.worlds.new("Studio fill");b.context.scene.world=world;world.color=(.32,.38,.44)
def finish(o,name,mat,bevel=0):
    o.name=name;o.data.materials.append(mat)
    if bevel:
        mod=o.modifiers.new("Machined edge","BEVEL");mod.width=bevel;mod.segments=3
        o.modifiers.new("Face normals","WEIGHTED_NORMAL")
    return o
def box(name,xyz,dim,mat,bevel=.015):
    b.ops.mesh.primitive_cube_add(size=1,location=xyz);o=b.context.object;o.dimensions=dim
    b.ops.object.transform_apply(location=False,rotation=False,scale=True)
    return finish(o,name,mat,bevel)
def cyl(name,xyz,r,h,mat,bev=0,verts=72):
    b.ops.mesh.primitive_cylinder_add(vertices=verts,radius=r,depth=h,location=xyz)
    return finish(b.context.object,name,mat,bev)
def ring(name,x,y,z,ro,ri,h,mat,N=104):
    pts=[(x+r*cos(2*pi*i/N),y+r*sin(2*pi*i/N),z+dz) for r,dz in [(ro,0),(ro,h),(ri,h),(ri,0)] for i in range(N)]
    faces=[(a*N+i,a*N+(i+1)%N,((a+1)%4)*N+(i+1)%N,((a+1)%4)*N+i) for a in range(4) for i in range(N)]
    mesh=b.data.meshes.new(name);mesh.from_pydata(pts,[],faces);mesh.update()
    o=b.data.objects.new(name,mesh);b.context.collection.objects.link(o);return finish(o,name,mat,.009)
def line(x,y,z,w,h,mat):return box("Inscribed line",(x,y,z),(w,h,.003),mat,0)
def setup(name):
    group=b.data.collections.new(name);b.context.scene.collection.children.link(group)
    b.context.view_layer.active_layer_collection=b.context.view_layer.layer_collection.children[name]
    return group
bench=setup("Workshop")
box("Benchtop",(0,0,-.20),(32,26,.39),slate,.04)
box("Blueprint",(0,.1,.018),(6.5,4.6,.032),ink)
for i in range(25):line((i-12)*.25,.1,.04,.009,4.2,teal)
for i in range(17):line(0,(i-8)*.25+.1,.04,6.15,.009,teal)
x,y=-.18,.36
fl=ring("Bearing flange",x,y,.055,1.40,.57,.29,steel)
for i in range(8):
    a=2*pi*(i+.5)/8;xx=x+1.09*cos(a);yy=y+1.09*sin(a)
    cutter=cyl("Drill", (xx,yy,.21),.155,.65,dark,0,40)
    mod=fl.modifiers.new("Bolt bore","BOOLEAN");mod.operation="DIFFERENCE";mod.object=cutter
    b.context.view_layer.objects.active=fl
    b.ops.object.modifier_apply(modifier=mod.name);b.data.objects.remove(cutter,do_unlink=True)
ring("Raised boss",x,y,.345,.904,.57,.30,steel)
ring("Upper chamfer",x,y,.646,.86,.57,.065,edge)
ring("Counterbore sleeve",x,y,.35,.578,.49,.31,brass)
for i in range(8):ring("Tool turning line",x,y,.343,1.16+i*.029,1.156+i*.029,.003,edge)
for i in range(5):ring("Boss turn",x,y,.710,.64+i*.044,.635+i*.044,.003,steel)
# A vernier caliper with fixed and sliding jaws, etched beam and thumb roller
box("Caliper beam",(.55,-1.42,.13),(4.25,.23,.12),steel,.025)
for i in range(73):
    line(-1.45+i*.052,-1.37,.193,.012,.09 if i%5==0 else .045,char)
for xx in [-1.48,.14]:
    box("Jaw shoulder",(xx,-1.16,.16),(.19,.65,.18),edge)
    jaw=box("Jaw tip",(xx+.045,-.80,.145),(.1,.24,.14),steel,.025);jaw.rotation_euler.z=.15
box("Vernier slider",(.25,-1.43,.22),(.69,.42,.13),teal)
for i in range(11):line(.009+i*.047,-1.48,.288,.012,.12,rule)
cyl("Adjustment wheel",(.32,-1.70,.18),.135,.13,brass,.01)
# Country still life miniatures
def sheet(name,x,y,z,w,h,accent,textlines=True):
    box(name,(x,y,z),(w,h,.055),paper,.026)
    line(x,y+h*.33,z+.03,w*.75,.085,accent)
    if textlines:
        for j in range(8):line(x-(.08*w if j%3==2 else 0),y+h*(.20-j*.074),z+.031,w*(.52 if j%3==2 else .69),.018,char)
de=setup("Two drafts");box("Archive desk",(0,0,-.12),(22,18,.23),ink)
for xx,accent in [(-1.24,teal),(1.24,brass)]:
    box("File cover",(xx,.0,.08),(2.26,2.95,.14),accent,.045);sheet("Draft document",xx,.07,.21,2.10,2.72,accent)
    box("Binder clip",(xx,.0+1.38,.32),(.43,.23,.13),dark)
au=setup("Recognition");box("Registry desk",(0,0,-.12),(22,18,.23),teal)
sheet("Training register",.98,.32,.15,2.7,2.9,ink)
box("Certificate folder",(-1.37,-.12,.24),(2.25,1.65,.18),ink,.045);sheet("Statement of attainment",-1.37,-.12,.38,2.10,1.47,teal,False)
for j in range(3):line(-1.54,.0-j*.15,.412,1.15,.025,char)
cyl("Embossed seal",(-.74,-.49,.424),.16,.03,brass,.007)
us=setup("Matching funds");box("Ledger table",(0,0,-.12),(22,18,.23),dark)
sheet("State plan",.94,.1,.19,2.25,2.85,teal);sheet("Federal ledger",-1.43,.05,.11,2.03,2.50,ink,False)
for yy in [-.35,.29]:
    for j in range(4):cyl("Matching funds token",(-1.36,yy,.19+j*.074),.34,.066,brass,.012)
for i in range(3):
    for j in range(2):
        xx=2.95+i*.48;yy=-.28+j*.80
        box("Classroom workbench",(xx,yy,.42),(.4,.53,.08),paper)
        for k in [-1,1]:box("Bench base",(xx+k*.13,yy,.21),(.07,.36,.4),teal)
lights=setup("Studio rig")
def area(pos,power,size,color):
    b.ops.object.light_add(type='AREA',location=pos);o=b.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.data.color=color;o.rotation_euler=(Vector((0,0,0))-o.location).to_track_quat('-Z','Y').to_euler()
area((-3,-4,7),1000,5,(.8,.94,1));area((4,4,6),1600,4,(1,.83,.62));area((-4,4,4),900,3,(.52,.9,1))
b.ops.object.camera_add();cam=b.context.object;b.context.scene.camera=cam
def view(pos,target,scale):
    cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=scale
scene=b.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=9;scene.cycles.use_denoising=True
scene.render.resolution_percentage=100;scene.render.resolution_x=1250;scene.render.resolution_y=890
scene.render.image_settings.file_format='WEBP';scene.render.image_settings.quality=89
def choose(group):
    for g in [bench,de,au,us]:g.hide_render=g!=group;g.hide_viewport=g!=group
def render(name,group,pos,target,scale):
    choose(group);view(pos,target,scale);scene.render.filepath=str(ROOT/'assets'/f'{name}.webp');b.ops.render.render(write_still=True)
choose(bench);view((4.3,-7,7),(.0,.0,.13),6.0)
b.ops.wm.save_as_mainfile(filepath=str(ROOT/'studio'/'workshop.blend'),compress=True)
b.ops.object.select_all(action='DESELECT')
for o in bench.objects:
    if o.name!='Benchtop':o.select_set(True)
b.ops.export_scene.gltf(filepath=str(ROOT/'assets'/'workshop.glb'),use_selection=True,export_apply=True,export_yup=True)
render('workshop',bench,(4.3,-7,7),(.0,.0,.13),6.3)
render('drafts',de,(2,-5,8),(0,0,.12),5.95)
render('register',au,(2,-5,7),(-.02,.02,.15),5.9)
render('ledger',us,(3,-6,7),(.52,0,.1),6.85)
render('inspection',bench,(1.2,-4,7),(-.15,.1,.3),3.95)

import trimesh
import numpy as np
from scipy.spatial.transform import Rotation as R
import  xml.dom.minidom


def xml2mesh(xml_file):
    dom = xml.dom.minidom.parse(xml_file)
    root = dom.documentElement
    body = root.getElementsByTagName('body')
    for b in body:
        name = b.getAttribute('name')
        child = b.childNodes
        mesh = []
        for c in child:
            if c.nodeType == 1:
                if c.nodeName == 'geom':
                    if c.getAttribute('type') == 'sphere':
                        size = c.getAttribute('size')
                        pos = c.getAttribute('pos')
                        mesh.append(create_sphere(pos,size))
                    elif c.getAttribute('type') == 'box':
                        pos = c.getAttribute('pos')
                        size = c.getAttribute('size')
                        mesh.append(create_box(pos, size))
                    else:
                        from_to = c.getAttribute('fromto')
                        size = c.getAttribute('size')
                        mesh.append(create_capsule(from_to, size))

        mesh_export(mesh, name)

def mesh_export(mesh, name):
    name = 'assets/human_body/body_mesh/' + name + '.obj'
    obj = mesh[0]
    if len(mesh) > 1:
        mesh.pop(0)
        v = obj.vertices
        f = obj.faces
        v = np.array(v)
        f = np.array(f)
        for m in mesh:
            v1 = m.vertices
            f1 = m.faces
            v1 = np.array(v1)
            f1 = np.array(f1)
            f1 = np.array(f1) + np.shape(v)[0]
            v = np.concatenate((v, v1), axis=0)
            f = np.concatenate((f, f1), axis=0)
        obj = trimesh.Trimesh(vertices=v, faces=f)
    obj.export(name)

def create_sphere(pos, size):
    if pos == '':
        pos = [0, 0, 0]
    else:
        pos = pos.split()
        for i in range(len(pos)):
            pos[i] = float(pos[i])
    R = np.identity(4)
    R[:3, 3] = np.array(pos).T
    R[3, :] = np.array([0, 0, 0, 1])
    mesh = trimesh.creation.icosphere(4, float(size))
    mesh.apply_transform(R)
    return mesh

def create_box(pos, size):
    if pos == '':
        pos = [0,0,0]
    else:
        pos = pos.split()
        for i in range(len(pos)):
            pos[i] = float(pos[i])
    size = size.split(' ')
    for i in range(len(size)):
        size[i] = float(size[i])*2
    R = np.identity(4)
    R[:3, 3] = np.array(pos).T
    R[3, :] = np.array([0, 0, 0, 1])
    mesh = trimesh.creation.box(size)
    mesh.apply_transform(R)
    return mesh

def create_capsule(from_to, size):
    pos = []
    vec2 = []
    from_to = from_to.split(' ')
    for i in range(len(from_to)):
        from_to[i] = float(from_to[i])
    for i in range(3):
        pos.append((from_to[i]+from_to[i+3])/2)
        vec2.append((from_to[i]-from_to[i+3]))
    pos = np.array(pos)
    height = sum(np.array(vec2) ** 2)
    height = pow(height, 0.5)
    vec1 = np.array([0, 0, 1.0])
    vec2 = vec2 / np.linalg.norm(vec2)
    if vec2[2] != 1:
        i = np.identity(3)
        v = np.cross(vec1, vec2)
        v_mat = [[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]]
        s = np.linalg.norm(v)
        c = np.dot(vec1, vec2)
        R_mat = i + v_mat + np.matmul(v_mat, v_mat) * (1 - c) / (s * s)
    else:
        R_mat = np.identity(3)
    T = np.identity(4)
    T[0:3, 0:3] = R_mat
    T[0:3, 3] = pos.T
    mesh = trimesh.creation.capsule(height, float(size))
    mesh.apply_transform(T)
    return mesh

def build_body(rot, trans, i, output):
    f = open('assets/human_body/index.txt')
    name = f.read()
    name = name.split()
    mesh = trimesh.load('assets/human_body/body_mesh/' + name[0] + '.obj')
    matrix = state2mat(trans[0], rot[0])
    mesh.apply_transform(matrix)
    v = np.array(mesh.vertices)
    f = np.array(mesh.faces)
    for j in range(1, len(rot)):
        mesh = trimesh.load('assets/human_body/body_mesh/' + name[j] + '.obj')
        matrix = state2mat(trans[j], rot[j])
        mesh.apply_transform(matrix)
        v2 = np.array(mesh.vertices)
        f2 = np.array(mesh.faces)
        f2 = np.array(f2) + np.shape(v)[0]
        v = np.concatenate((v, v2), axis=0)
        f = np.concatenate((f, f2), axis=0)
        obj = trimesh.Trimesh(vertices=v, faces=f)
    obj.export(output+'/full_body'+str(i)+'.obj')

def state2mat(pos, rot):
    Rm = R.from_quat(rot)
    matrix_l = np.hstack((Rm.as_matrix(), np.mat(pos).T))
    matrix_l = np.vstack((matrix_l, np.mat([0, 0, 0, 1])))
    return matrix_l.A

if __name__ == '__main__':
    xml_file = "assets/human_body/amp_humanoid.xml"
    xml2mesh(xml_file)
    
    import os
    demo_name = 'multiobj_multistep_2'
    outpath = "assets/human_body/"+demo_name
    if not os.path.exists(outpath):
        os.mkdir(outpath)

    motion_data = np.load('assets/motion_sequence/'+demo_name+'.npy', allow_pickle=True).item()
    rot = motion_data['rot']
    trans = motion_data['trans']

    for i in range(600):
        build_body(rot[i], trans[i], i, outpath)
        print(i)










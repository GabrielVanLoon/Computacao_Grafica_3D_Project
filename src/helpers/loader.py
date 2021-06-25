
def load_model_from_file(filename):
    """Loads a Wavefront OBJ file. """

    objects  = {}
    vertices = []
    normals  = []
    texture_coords = []
    faces = []

    material = None

    # Open wavefront file and read line by line
    for line in open(filename, "r"): 

        # Comentario
        if line.startswith('#'): continue ## ignora comentarios

        # Quebra da linha em espaços
        values = line.split()

        # Se a linha estiver fazia ignora
        if not values: 
            continue

        # Recuperando Vertices de Posição (3 coords)
        if values[0] == 'v':
            vertices.append(values[1:4])

        # Recuperando Vetores Normais (3 coords)
        elif values[0] == 'vn':
            normals.append(values[1:4])

        # Recuperando Coordenadas de textura (2 coords)
        elif values[0] == 'vt':
            texture_coords.append(values[1:3])

        # Defininto o meterial do objeto (O que é mesmo)?
        elif values[0] in ('usemtl', 'usemat'):
            material = values[1]

        # Definindo as faces
        elif values[0] == 'f':
            face = []
            face_texture = []
            face_normals = []

            for v in values[1:]:
                w = v.split('/')
                face.append(int(w[0]))
                face_normals.append(int(w[2]))
                if len(w) >= 2 and len(w[1]) > 0:
                    face_texture.append(int(w[1]))
                else:
                    face_texture.append(0)

            faces.append((face, face_texture, face_normals, material))

    model = {}
    model['vertices'] = vertices
    model['texture'] = texture_coords
    model['faces'] = faces
    model['normals'] = normals

    return model

if __name__ == "__main__":
    print(load_model_from_file("../../assets/objects/cube.obj")['faces'])
#version 330 core
layout(location=0) in uvec3 in_position;
layout(location=1) in uint  in_voxel_id;
layout(location=2) in uint  in_face_id;

out vec3 out_color;

uniform mat4 m_model;
uniform mat4 m_view;
uniform mat4 m_projection;


vec3 get_color(float p) {
    vec3 p3 = fract(vec3(p * 21.2) * vec3(0.1031, 0.1029, 0.0973));
    p3 += dot(p3, p3.yzx + 19.19);
    return fract((p3.xxy + p3.yzz) * p3.zyx) + 0.05;
}

void main(){
  gl_Position = m_projection * m_view * m_model * vec4(in_position, 1.0f);

  out_color = get_color(in_voxel_id);
  if (in_face_id == 0u) {
    // out_color = vec4(0.0f,1.0f,1.0f, 1.0f);
    out_color = vec3(in_voxel_id * 0.1, in_face_id * 0.1, 0.5);
  }
  // out_color = vec4(0.6f,0.4f,0.5f, 1.0f);
}

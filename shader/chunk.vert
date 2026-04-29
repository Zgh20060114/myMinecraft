#version 330 core
layout(location=0) in uvec3 in_position;
layout(location=1) in uint  in_voxel_id;
layout(location=2) in uint  in_face_id;

out vec4 out_color;

uniform mat4 m_model;
uniform mat4 m_view;
uniform mat4 m_projection;


void main(){
  gl_Position = m_projection * m_view * m_model * vec4(in_position, 1.0f);

  if (in_face_id == 0u) {
    out_color = vec4(1.0f,0.0f,0.0f, 1.0f);
  }

  if (in_face_id == 1u) {
    out_color = vec4(0.0f,1.0f,0.0f, 1.0f);
  }
  if (in_face_id == 2u) {
    out_color = vec4(0.0f,0.0f,1.0f, 1.0f);
  }
  if (in_face_id == 3u) {
    out_color = vec4(1.0f,1.0f,0.0f, 1.0f);
  }
  if (in_face_id == 4u) {
    out_color = vec4(1.0f,0.0f,1.0f, 1.0f);
  }
  if (in_face_id == 5u) {
    // out_color = vec4(0.0f,1.0f,1.0f, 1.0f);
    out_color = vec4(in_voxel_id * 0.1, in_face_id * 0.1, 0.5, 1.0);
  }
  // out_color = vec4(0.6f,0.4f,0.5f, 1.0f);
}

#version 330 core
layout(location=0) in uvec3 in_position;
layout(location=1) in uvec2 in_texture_coord;

out vec2 out_uv;
out vec3 out_box_color;

uniform mat4 m_model;
uniform mat4 m_view;
uniform mat4 m_projection;
uniform uint selected_mode;

const vec3 box_color = vec3(1,0,0);

void main(){
  gl_Position = m_projection * m_view * m_model * vec4((in_position-0.5)*1.01+0.5, 1.0f);
  out_uv = in_texture_coord;
  out_box_color = box_color;
}

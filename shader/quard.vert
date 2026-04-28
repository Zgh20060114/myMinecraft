#version 330 core
layout(location=0) in vec3 in_position;
layout(location=1) in vec3 in_color;
out vec4 out_color;

uniform mat4 m_model;
uniform mat4 m_view;
uniform mat4 m_projection;


void main(){
  gl_Position = m_projection * m_view * m_model * vec4(in_position, 1.0f);
  out_color = vec4(in_color, 1.0f);
}

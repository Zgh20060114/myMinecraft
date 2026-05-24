#version 330 core
layout(location=0) in uvec3 in_vertex_position;
layout(location=1) in uvec2 in_texture_coord;
out vec2 out_texture_coord;

uniform mat4 m_view;
uniform mat4 m_projection;
uniform int water_amplify_scale;
uniform float water_line;


void main(){
  vec3 water_vertex_position = vec3(in_vertex_position);
  water_vertex_position.xz *= water_amplify_scale;
  water_vertex_position.xz -= 0.5* water_amplify_scale;
  water_vertex_position.y = water_line;
  out_texture_coord = vec2(in_texture_coord) * water_amplify_scale; 
  gl_Position = m_projection * m_view  * vec4(water_vertex_position, 1.0f);
}

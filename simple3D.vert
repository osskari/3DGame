attribute vec3 a_position;
attribute vec3 a_normal;
attribute vec2 a_uv;

uniform vec4 u_color;

uniform mat4 u_model_matrix;
uniform mat4 u_view_matrix;
uniform mat4 u_projection_matrix;

uniform vec4 u_light_position;
uniform vec4 u_sun_position;
uniform vec4 u_moon_position;
uniform vec4 u_eye_position; 

varying vec4 v_normal;
varying vec4 v_s;
varying vec4 v_h;

varying vec4 v_s_sun;
varying vec4 v_h_sun;

varying vec4 v_s_moon;
varying vec4 v_h_moon;

varying vec2 v_uv;

void main(void)
{
	// Local coordinates
	vec4 position = vec4(a_position.x, a_position.y, a_position.z, 1.0);
	vec4 normal = vec4(a_normal.x, a_normal.y, a_normal.z, 0.0);

	// UV coordinates sent into per-pixel use;
	v_uv = a_uv;

	//v_normal that is used in the fragment shader
	v_normal = normalize(u_model_matrix * normal);
	// Global coordinates
	position = u_model_matrix * position;


	//Calculate the vector from the material to the light
	//and the vector from the material to the eye
	//then calculate the halfway vector
	v_s = normalize(u_light_position - position);
	v_s_sun = normalize(u_sun_position - position);
	v_s_moon = normalize(u_moon_position - position);
	vec4 v = normalize(u_eye_position - position);
	v_h = normalize(v_s + v);
	v_h_sun = normalize(v_s_sun + v);
	v_h_moon = normalize(v_s_moon + v);

	// Eye coordiantes
	position = u_view_matrix * position;

	// Clip coordinates
	position = u_projection_matrix * position;

	// output value of the vertex shader
	gl_Position = position;
}
attribute vec3 a_position;
attribute vec2 a_uv;


uniform mat4 u_model_matrix;
uniform mat4 u_view_matrix;
uniform mat4 u_projection_matrix;


varying vec2 v_uv;

void main(void)
{
	// Local coordinates
	vec4 position = vec4(a_position.x, a_position.y, a_position.z, 1.0);

	// UV coordinates sent into per-pixel use;
	v_uv = a_uv;

	// Global coordinates
	position = u_model_matrix * position;

	// Eye coordiantes
	position = u_view_matrix * position;

	// Clip coordinates
	position = u_projection_matrix * position;

	// output value of the vertex shader
	gl_Position = position;
}
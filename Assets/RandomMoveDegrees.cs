using UnityEngine;
using System.Collections;
using UnityEngine.UI;

public class RandomMoveDegrees : MonoBehaviour
{
	// left sensor
	public Transform sensor1;
	// right sensor
	public Transform sensor2;

	public Transform grassDisplay;
	public Transform timeDisplay;
	public Transform sensor1Distance;
	public Transform sensor2Distance;
	public Transform startPoint1;
	public Transform startPoint2;

	int maxAmountOfGrass = 0;
	const float maxSpeed = 1.0f;
	float speed = maxSpeed;

	float distanceToObstacle1 = 1;
	float distanceToObstacle2 = 1;
	float lastDistanceToObstacle1 = 1;
	float lastDistanceToObstacle2 = 1;


	// Use this for initialization
	void Start ()
	{
		maxAmountOfGrass = GameObject.FindGameObjectsWithTag ("Grass").Length;
		speed = maxSpeed;
		transform.position = startPoint1.position;
	}
	
	// Update is called once per frame
	void Update ()
	{
		transform.Translate (Vector3.forward * Time.deltaTime * speed);			

		float timer = Time.realtimeSinceStartup;
		float minutes = Mathf.Floor (timer / 60);
		float seconds = timer % 60;
		string niceTime = string.Format ("Time lapsed: {0:00}:{1:00}", minutes, seconds);
		timeDisplay.GetComponent<Text> ().text = niceTime;

		int amountOfGrass = GameObject.FindGameObjectsWithTag ("Grass").Length;
		float percentA = ((100f / maxAmountOfGrass) * amountOfGrass);
		float percent = Mathf.Floor (percentA);
		string nicepercent = string.Format ("Amount of grass: {0:00} %", percent);

		grassDisplay.GetComponent<Text> ().text = nicepercent;

		string niceDist1 = string.Format ("Distance sensor1: {0}", distanceToObstacle1);
		string niceDist2 = string.Format ("Distance sensor2: {0}", distanceToObstacle2);
		sensor1Distance.GetComponent<Text> ().text = "" + niceDist1;
		sensor2Distance.GetComponent<Text> ().text = "" + niceDist2;

		if (seconds >= 10) {
			transform.position = startPoint2.position;
			transform.GetComponent<Rigidbody> ().useGravity = true;
		}
		if (seconds >= 40) {
			transform.position = startPoint1.position;
		}
	}

	void FixedUpdate ()
	{
		RaycastHit hit;

		int layer_mask = LayerMask.GetMask ("ObjectsForUltrasonic");

		// Cast a sphere wrapping character controller 10 meters forward
		// to see if it is about to hit anything.
		if (Physics.SphereCast (sensor1.position - (sensor1.forward * 0.1f), 0.1f, sensor1.forward, out hit, 4, layer_mask)) {
			distanceToObstacle1 = hit.distance;
			Debug.DrawLine (sensor1.position, hit.point);
		}
		if (Physics.SphereCast (sensor2.position - (sensor2.forward * 0.1f), 0.1f, sensor2.forward, out hit, 4, layer_mask)) {
			distanceToObstacle2 = hit.distance;
			Debug.DrawLine (sensor2.position, hit.point);
		}

		int range = Random.Range (180, 270);
		//int range = Random.Range (165, 285);
		//int range = Random.Range (150, 300);
		if (distanceToObstacle1 < 0.1f || distanceToObstacle2 < 0.11f) {
			speed = 0;
			transform.Rotate (Vector3.up, range);
			speed = maxSpeed;
		}

		// measure again
		if (Physics.SphereCast (sensor1.position - (sensor1.forward * 0.1f), 0.1f, sensor1.forward, out hit, 4, layer_mask)) {
			distanceToObstacle1 = hit.distance;
			Debug.DrawLine (sensor1.position, hit.point);
		}
		if (Physics.SphereCast (sensor2.position - (sensor2.forward * 0.1f), 0.1f, sensor2.forward, out hit, 4, layer_mask)) {
			distanceToObstacle2 = hit.distance;
			Debug.DrawLine (sensor2.position, hit.point);
		}

		if ((lastDistanceToObstacle1 < 0.2f && distanceToObstacle1 < 0.11f) ||
		    (lastDistanceToObstacle2 < 0.2f && distanceToObstacle2 < 0.11f)) {

			// if it is still the same range 
			while ((distanceToObstacle1 < 0.5f) ||
			       (distanceToObstacle2 < 0.5f)) {

				lastDistanceToObstacle1 = distanceToObstacle1;
				lastDistanceToObstacle2 = distanceToObstacle2;

				transform.Rotate (Vector3.up, 10);

				// measure again
				if (Physics.SphereCast (sensor1.position - (sensor1.forward * 0.1f), 0.1f, sensor1.forward, out hit, 4, layer_mask)) {
					distanceToObstacle1 = hit.distance;
					Debug.DrawLine (sensor1.position, hit.point);
				}
				if (Physics.SphereCast (sensor2.position - (sensor2.forward * 0.1f), 0.1f, sensor2.forward, out hit, 4, layer_mask)) {
					distanceToObstacle2 = hit.distance;
					Debug.DrawLine (sensor2.position, hit.point);
				}
			}
		}

		lastDistanceToObstacle1 = distanceToObstacle1;
		lastDistanceToObstacle2 = distanceToObstacle2;

	}

	void OnCollisionEnter (Collision collision)
	{
		if (collision.gameObject.tag.Equals ("Grass")) {
			Destroy (collision.gameObject);
		} else if (!collision.gameObject.tag.Equals ("Ground")) {
			Debug.Log ("Blub");
			/*speed = 0;
			transform.Translate (Vector3.back * Time.deltaTime * 2);
			transform.Rotate (Vector3.up, Random.Range (180, 270));
			speed = maxSpeed;*/
		} 	
	}

}

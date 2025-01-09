// wip1 Quantum Encoding using superdense coding concepts

#include	<iostream>	// i/o functionality

#include	<fstream>	// read and write to files
#include	<cmath>		// provide mathematical functions
#include	<cstdlib>	// general purposes (random generator)
#include	<ctime>		// manipulate date and time
#include	<lame/lame.h>	// mp3 encoder

using namespace std;

const int SAMPLE_RATE = 44100;
const int BIT_RATE = 128;	// in kbps

// Generate a sine wave of a specific frequency and duration
void generateSineWave(float frequency, float duration, short* buffer, int& numSamples) {
	numSamples = static_cast<int>(SAMPLE_RATE * duration);
	for (int i = 0; i < numSamples; ++i) {
		buffer[i] = static_cast<short>(32767 * sin(2 * M_PI * frequency * i / SAMPLE_RATE));
	}
}

void writeMP3(const std::string& filename, short* buffer, int numSamples) {

	lame_t lame = lame_init();	// initializes lame encoder
	lame_set_in_samplerate(lame, SAMPLE_RATE);	// sets the sample rate
	lame_set_brate(lame, BIT_RATE);	// set the bitrate
	lame_set_quality(lame, 2);	// High quality (2)
	lame_init_params(lame);		// finalizes parameter setup

	ofstream outFile(filename, ios::binary);
	if (!outFile) {
		cerr << "Failed to open output file!" << endl;
		lame_close(lame);
		return;
	}

	const int MP3_BUFFER_SIZE = 7200 + numSamples * 5 / 4;
	unsigned char* mp3Buffer = new unsigned char[MP3_BUFFER_SIZE];

	// Converts raw audio samples (sine wave) into mp3 format.
	// buffer = raw audio data
	int mp3Size = lame_encode_buffer_interleaved(lame, buffer, numSamples, mp3Buffer, MP3_BUFFER_SIZE);

	if (mp3Size < 0) {
		cerr << "Error encoding MP3: " << mp3Size << endl;
	} else {
		outFile.write(reinterpret_cast<char*>(mp3Buffer), mp3Size);
	}

	int flushSize = lame_encode_flush(lame, mp3Buffer, MP3_BUFFER_SIZE);
	if (flushSize > 0) {
		outFile.write(reinterpret_cast<char*>(mp3Buffer), flushSize);
	}

	delete[] mp3Buffer;
	lame_close(lame);
	outFile.close();
}

int main(void)
{
	srand(time(nullptr));

	float duration;
	duration = 3;		//  time duration of the mp3 file in seconds
	
	/* 
	 * Generation of a random frequency between 200 and 1000Hz
	 * 200.0f = minimum frequency
	 * random float between 0 and 1 generated
	 * multiply by 800.0f scales it to the correct range
	 */

	float randomFrequency = 200.0f + static_cast<float>(rand()) / RAND_MAX * 800.0;
											cout << "Generating sin wave of frequency: " << randomFrequency << " Hz for " << duration << " seconds." << endl;

											int numSamples;
	short* buffer = new short[static_cast<int>(SAMPLE_RATE * duration)];
	generateSineWave(randomFrequency, duration, buffer, numSamples);

	string filename = "sine_wave.mp3";
	writeMP3(filename, buffer, numSamples);

	delete[] buffer;

	cout << "MP3 file generated: " << filename << endl;
	return 0;
}

#pragma once

#ifndef INPUT_SIM_H
#define INPUT_SIM_H

// ccgs: Wrappers for win functions that simulate keyboard and mouse inputs

namespace input_sim
{
	void simulateKeySequence(std::vector<byte> aucVK, bool bContinueSeq = false);
	void simulateKeyPressed(byte ucVK);
	void simulateMouseClicked();
}

#endif

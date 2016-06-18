
// Mt5UI.h : main header file for the Mt5UI application
//
#pragma once

#ifndef __AFXWIN_H__
	#error "include 'stdafx.h' before including this file for PCH"
#endif

#include "resource.h"       // main symbols

// CMt5UIApp:
// See Mt5UI.cpp for the implementation of this class
//

class CMt5UIApp : public CWinAppEx
{
public:
	CMt5UIApp();
private:
// Overrides
public:
	virtual BOOL InitInstance();
	virtual int ExitInstance();

// Implementation
	UINT  m_nAppLook;
	BOOL  m_bHiColorIcons;

	virtual void PreLoadState();
	virtual void LoadCustomState();
	virtual void SaveCustomState();

	afx_msg void OnAppAbout();
	DECLARE_MESSAGE_MAP()
};

extern CMt5UIApp theApp;

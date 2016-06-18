
// Mt5UIView.h : interface of the CMt5UIView class
//

#pragma once


class CMt5UIView : public CEditView
{
protected: // create from serialization only
	CMt5UIView();
	DECLARE_DYNCREATE(CMt5UIView)

// Attributes
public:
	CMt5UIDoc* GetDocument() const;

// Operations
public:

// Overrides
public:
	virtual BOOL PreCreateWindow(CREATESTRUCT& cs);
protected:

// Implementation
public:
	virtual ~CMt5UIView();
#ifdef _DEBUG
	virtual void AssertValid() const;
	virtual void Dump(CDumpContext& dc) const;
#endif

protected:

// Generated message map functions
protected:
	afx_msg void OnFilePrintPreview();
	afx_msg void OnRButtonUp(UINT nFlags, CPoint point);
	afx_msg void OnContextMenu(CWnd* pWnd, CPoint point);
	DECLARE_MESSAGE_MAP()
};

#ifndef _DEBUG  // debug version in Mt5UIView.cpp
inline CMt5UIDoc* CMt5UIView::GetDocument() const
   { return reinterpret_cast<CMt5UIDoc*>(m_pDocument); }
#endif


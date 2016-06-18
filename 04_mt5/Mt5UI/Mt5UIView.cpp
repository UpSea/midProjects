
// Mt5UIView.cpp : implementation of the CMt5UIView class
//

#include "stdafx.h"
// SHARED_HANDLERS can be defined in an ATL project implementing preview, thumbnail
// and search filter handlers and allows sharing of document code with that project.
#ifndef SHARED_HANDLERS
#include "Mt5UI.h"
#endif

#include "Mt5UIDoc.h"
#include "Mt5UIView.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif


// CMt5UIView

IMPLEMENT_DYNCREATE(CMt5UIView, CEditView)

BEGIN_MESSAGE_MAP(CMt5UIView, CEditView)
	ON_WM_CONTEXTMENU()
	ON_WM_RBUTTONUP()
END_MESSAGE_MAP()

// CMt5UIView construction/destruction

CMt5UIView::CMt5UIView()
{
	// TODO: add construction code here

}

CMt5UIView::~CMt5UIView()
{
}

BOOL CMt5UIView::PreCreateWindow(CREATESTRUCT& cs)
{
	// TODO: Modify the Window class or styles here by modifying
	//  the CREATESTRUCT cs

	BOOL bPreCreated = CEditView::PreCreateWindow(cs);
	cs.style &= ~(ES_AUTOHSCROLL|WS_HSCROLL);	// Enable word-wrapping

	return bPreCreated;
}

void CMt5UIView::OnRButtonUp(UINT /* nFlags */, CPoint point)
{
	ClientToScreen(&point);
	OnContextMenu(this, point);
}

void CMt5UIView::OnContextMenu(CWnd* /* pWnd */, CPoint point)
{
#ifndef SHARED_HANDLERS
	theApp.GetContextMenuManager()->ShowPopupMenu(IDR_POPUP_EDIT, point.x, point.y, this, TRUE);
#endif
}


// CMt5UIView diagnostics

#ifdef _DEBUG
void CMt5UIView::AssertValid() const
{
	CEditView::AssertValid();
}

void CMt5UIView::Dump(CDumpContext& dc) const
{
	CEditView::Dump(dc);
}

CMt5UIDoc* CMt5UIView::GetDocument() const // non-debug version is inline
{
	ASSERT(m_pDocument->IsKindOf(RUNTIME_CLASS(CMt5UIDoc)));
	return (CMt5UIDoc*)m_pDocument;
}
#endif //_DEBUG


// CMt5UIView message handlers
